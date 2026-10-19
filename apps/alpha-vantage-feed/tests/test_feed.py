import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import feed


def gold(value='4200'):
    return {'structuredContent': {'nominal': 'XAUUSD', 'timestamp': '2026-10-18 16:47:34', 'price': value}}


def daily(name='Crude Oil Prices WTI', unit='dollars per barrel'):
    return {'structuredContent': {'preview': True, 'sample_data': json.dumps({'name': name, 'interval': 'daily', 'unit': unit, 'data': [
        {'date': '2026-10-17', 'value': '.'}, {'date': '2026-10-14', 'value': '100'}, {'date': '2026-10-15', 'value': '101'}]})}}


class Client:
    def __init__(self, result):
        self.result = result
        self.calls = []
    def call(self, name, args):
        self.calls.append((name, args))
        return self.result


class FeedTests(unittest.TestCase):
    def test_sources_timestamps_numeric_and_preview(self):
        now = feed.utcnow()
        m = feed.normalize('gold', gold(), now)
        self.assertEqual(m['timezone'], 'not supplied')
        self.assertEqual(m['observed_at'], '2026-10-18 16:47:34')
        self.assertEqual(m['retrieved_at'], now)
        self.assertEqual(feed.normalize('wti', daily(), now)['observed_at'], '2026-10-15')
        for value in ['nan', 'inf', '-5', '0']:
            with self.assertRaises(feed.FeedError):
                feed.normalize('gold', gold(value), now)
        with self.assertRaises(feed.FeedError):
            feed.normalize('us10y', daily('2-Year Treasury Constant Maturity Rate', 'percent'), now)
        with self.assertRaises(feed.ProviderRefusal):
            feed.unwrap({'isError': False, 'structuredContent': {'error': {'type': 'rate_limit'}}})
        with self.assertRaises(feed.ProviderRefusal):
            feed.unwrap({'content': [{'type': 'text', 'text': '{"Information":"limit"}'}]})
        with self.assertRaises(feed.FeedError):
            feed.unwrap({'isError': True})

    def test_budget_persists_retention_and_rate_limit_stops_run(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'state.sqlite3'
            cache = feed.Cache(path)
            old = feed.normalize('gold', gold(), '2020-01-01T00:00:00+00:00')
            cache.save({'market_data': {'gold': old}, 'attempts': {}})
            client = Client({'structuredContent': {'error': {'type': 'rate_limit'}}})
            result = feed.collect(cache, client, limit=1)
            self.assertEqual(len(client.calls), 1)
            self.assertEqual(result['market_data']['gold'], old)
            cache.db.close()
            reopened = feed.Cache(path)
            self.assertFalse(reopened.reserve(1))
            self.assertEqual(reopened.get()['market_data']['gold']['retrieved_at'], old['retrieved_at'])
            reopened.db.close()

    def test_cache_does_not_spend_requests(self):
        with tempfile.TemporaryDirectory() as directory:
            cache = feed.Cache(Path(directory)/'state.sqlite3')
            cache.save({'market_data': {k: {'retrieved_at': feed.utcnow()} for k in feed.SPECS}, 'attempts': {}})
            client = Client({})
            feed.collect(cache, client)
            self.assertEqual(client.calls, [])
            cache.db.close()

    def test_stdio_discovery_initialization_and_allowlist(self):
        fake = '''import sys,json
for line in sys.stdin:
 m=json.loads(line)
 if 'id' not in m: continue
 if m['method']=='initialize': r={'protocolVersion':'2025-03-26','capabilities':{}}
 elif m['method']=='tools/list': r={'tools':[{'name':'GOLD_SILVER_SPOT'}]}
 elif m['method']=='tools/call': r={'structuredContent':{'nominal':'XAUUSD','timestamp':'2026-10-18 12:00:00','price':'4200'}}
 else: r={}
 print(json.dumps({'jsonrpc':'2.0','id':m['id'],'result':r}),flush=True)
'''
        with feed.MCP([sys.executable, '-u', '-c', fake]) as client:
            self.assertIn('GOLD_SILVER_SPOT', client.tools)
            self.assertEqual(feed.normalize('gold', client.call('GOLD_SILVER_SPOT', {'symbol': 'GOLD'}), feed.utcnow())['value'], 4200)
            with self.assertRaises(feed.FeedError):
                client.call('ORDER_SEND', {})

    def test_local_api_and_dashboard_use_same_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'state.sqlite3'
            cache = feed.Cache(path)
            cache.save({'market_data': {'gold': feed.normalize('gold', gold(), feed.utcnow())}, 'attempts': {}})
            cache.db.close()
            server = ThreadingHTTPServer(('127.0.0.1', 0), feed.handler_for(path))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = 'http://127.0.0.1:'+str(server.server_port)
                with urlopen(base+'/api/market') as response:
                    self.assertEqual(json.load(response)['market_data']['gold']['value'], 4200)
                    self.assertEqual(response.headers['Cache-Control'], 'no-store')
                with urlopen(base) as response:
                    html = response.read().decode()
                    self.assertIn('/api/market', html)
                    self.assertNotIn('API_KEY', html)
            finally:
                server.shutdown()
                server.server_close()
                thread.join()


if __name__ == '__main__':
    unittest.main()
