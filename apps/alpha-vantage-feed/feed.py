#!/usr/bin/env python3
"""Read-only Alpha Vantage stdio MCP collector and loopback snapshot dashboard."""
import argparse
import json
import math
import os
from pathlib import Path
import queue
import sqlite3
import subprocess
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parent
SPECS = {
    'gold': ('GOLD_SILVER_SPOT', {'symbol': 'GOLD'}, 0),
    'btc': ('CURRENCY_EXCHANGE_RATE', {'from_currency': 'BTC', 'to_currency': 'USD'}, 0),
    'wti': ('WTI', {'interval': 'daily'}, 86400),
    'brent': ('BRENT', {'interval': 'daily'}, 86400),
    'us10y': ('TREASURY_YIELD', {'interval': 'daily', 'maturity': '10year'}, 86400),
}


def utcnow():
    return datetime.now(timezone.utc).isoformat()


class FeedError(Exception):
    """A provider/transport failure; deliberately excludes secret-bearing payloads."""


class ProviderRefusal(FeedError):
    pass


class MCP:
    """One serialized MCP session. Provider key is inherited from environment only."""
    def __init__(self, command=None):
        self.command = command or ['uvx', '--python', '3.13', 'marketdata-mcp-server']
        self.seq = 0
        self.messages = queue.Queue()
        self.last_call = 0

    def __enter__(self):
        self.proc = subprocess.Popen(self.command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.DEVNULL, text=True, bufsize=1)
        def read():
            for line in self.proc.stdout:
                try:
                    self.messages.put(json.loads(line))
                except ValueError:
                    continue
            self.messages.put(None)
        self.reader = threading.Thread(target=read, daemon=True)
        self.reader.start()
        try:
            self.rpc('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                                   'clientInfo': {'name': 'gold-reference-collector', 'version': '1.0'}})
            self.send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
            self.tools = set()
            cursor = None
            while True:
                page = self.rpc('tools/list', {'cursor': cursor} if cursor else {})
                self.tools.update(t['name'] for t in page.get('tools', []))
                cursor = page.get('nextCursor')
                if not cursor:
                    break
            return self
        except Exception:
            self.__exit__(None, None, None)
            raise

    def send(self, message):
        try:
            self.proc.stdin.write(json.dumps(message) + '\n')
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as exc:
            raise FeedError('MCP connection closed') from exc

    def rpc(self, method, params):
        self.seq += 1
        self.send({'jsonrpc': '2.0', 'id': self.seq, 'method': method, 'params': params})
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            try:
                result = self.messages.get(timeout=max(.01, deadline-time.monotonic()))
            except queue.Empty as exc:
                raise FeedError('MCP response timed out') from exc
            if result is None:
                raise FeedError('MCP server stopped')
            if result.get('id') == self.seq:
                if 'error' in result:
                    raise FeedError('MCP request failed')
                return result.get('result', {})
        raise FeedError('MCP response timed out')

    def call(self, name, arguments):
        if name not in self.tools or name not in {s[0] for s in SPECS.values()}:
            raise FeedError('Required read tool is unavailable')
        time.sleep(max(0, 1.1 - (time.monotonic()-self.last_call)))
        self.last_call = time.monotonic()
        return self.rpc('tools/call', {'name': name, 'arguments': arguments})

    def __exit__(self, *_):
        self.proc.terminate()
        try:
            self.proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proc.kill()
            self.proc.wait()
        self.reader.join(timeout=1)
        self.proc.stdin.close()
        self.proc.stdout.close()


def unwrap(result):
    if result.get('isError'):
        raise FeedError('Provider tool failed')
    data = result.get('structuredContent')
    if not data:
        try:
            data = json.loads(next(c['text'] for c in result.get('content', []) if c.get('type') == 'text'))
        except (StopIteration, ValueError, KeyError) as exc:
            raise FeedError('Provider response is not JSON') from exc
    if not isinstance(data, dict):
        raise FeedError('Unexpected provider response')
    for _ in range(2):
        if any(k in data for k in ['error', 'Error Message', 'Information', 'Note']):
            raise ProviderRefusal('Provider refused request (quota, access or parameters); no retry')
        if data.get('preview'):
            try:
                data = json.loads(data['sample_data'])
            except (ValueError, KeyError, TypeError) as exc:
                raise FeedError('Invalid provider preview') from exc
            if not isinstance(data, dict):
                raise FeedError('Invalid provider preview')
        else:
            return data
    raise FeedError('Unsupported nested provider preview')


def normalize(key, result, retrieved_at):
    data = unwrap(result)
    if key == 'gold':
        raw, observed, zone, instrument, unit = data['price'], data['timestamp'], 'not supplied', data['nominal'], 'USD per troy ounce'
        if instrument != 'XAUUSD':
            raise FeedError('Unexpected gold instrument')
        note = 'Provider reference; timezone/delay unspecified; not MT5 bid/ask.'
    elif key == 'btc':
        d = data['Realtime Currency Exchange Rate']
        if d['1. From_Currency Code'] != 'BTC' or d['3. To_Currency Code'] != 'USD':
            raise FeedError('Unexpected BTC pair')
        raw, observed, zone, instrument, unit = d['5. Exchange Rate'], d['6. Last Refreshed'], d['7. Time Zone'], 'BTC/USD', 'USD per BTC'
        note = 'Venue unspecified; not a broker execution price.'
    else:
        if data.get('interval') != 'daily':
            raise FeedError('Unexpected series interval')
        rows = []
        for row in data['data']:
            if row['value'] == '.':
                continue
            try:
                v = float(row['value'])
                datetime.strptime(row['date'], '%Y-%m-%d')
            except (ValueError, TypeError):
                continue
            if math.isfinite(v) and v > 0:
                rows.append(row)
        if not rows:
            raise FeedError('No valid daily observation')
        row = max(rows, key=lambda r: r['date'])
        raw, observed, zone, instrument, unit = row['value'], row['date'], 'date only', data['name'], data['unit']
        if unit != ('percent' if key == 'us10y' else 'dollars per barrel'):
            raise FeedError('Unexpected observation unit')
        if key == 'us10y' and '10-Year' not in instrument:
            raise FeedError('Unexpected Treasury maturity')
        if key in ('wti', 'brent') and key.lower() not in instrument.lower():
            raise FeedError('Unexpected oil series')
        note = 'Nominal yield; not real yield.' if key == 'us10y' else 'Daily EIA/FRED series; published with lag; not a futures quote.'
    value = float(raw)
    if not math.isfinite(value) or value <= 0:
        raise FeedError('Invalid numeric observation')
    datetime.fromisoformat(observed.replace('Z', '+00:00'))  # Validate; preserve raw timezone semantics.
    return {'provider': 'Alpha Vantage', 'function': SPECS[key][0], 'value': value,
            'instrument': instrument, 'unit': unit, 'observed_at': observed, 'timezone': zone,
            'retrieved_at': retrieved_at, 'kind': 'reference quote' if key in ('gold', 'btc') else 'daily observation', 'note': note}


class Cache:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS usage (day TEXT PRIMARY KEY, count INTEGER NOT NULL)')
        self.db.commit()

    def get(self):
        row = self.db.execute("SELECT value FROM state WHERE key='snapshot'").fetchone()
        return json.loads(row[0]) if row else {'market_data': {}, 'attempts': {}}

    def save(self, snapshot):
        self.db.execute("INSERT OR REPLACE INTO state VALUES ('snapshot', ?)", (json.dumps(snapshot, allow_nan=False),))
        self.db.commit()

    def reserve(self, limit):
        # IMMEDIATE transaction prevents concurrent processes overspending this local counter.
        day = datetime.now(timezone.utc).date().isoformat()
        self.db.execute('BEGIN IMMEDIATE')
        try:
            self.db.execute('INSERT OR IGNORE INTO usage VALUES (?, 0)', (day,))
            used = self.db.execute('SELECT count FROM usage WHERE day=?', (day,)).fetchone()[0]
            if used >= limit:
                self.db.rollback()
                return False
            self.db.execute('UPDATE usage SET count=count+1 WHERE day=?', (day,))
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise


def collect(cache, client, limit=12, quote_ttl=21600):
    snapshot = cache.get()
    for key, (tool, args, ttl) in SPECS.items():
        prior = snapshot['market_data'].get(key)
        age = time.time() - datetime.fromisoformat(prior['retrieved_at']).timestamp() if prior else math.inf
        if age < (ttl or quote_ttl):
            continue
        at = utcnow()
        if not cache.reserve(limit):
            snapshot['attempts'][key] = {'at': at, 'status': 'budget exhausted; retained prior observation'}
        else:
            try:
                snapshot['market_data'][key] = normalize(key, client.call(tool, args), utcnow())
                snapshot['attempts'][key] = {'at': at, 'status': 'success'}
            except ProviderRefusal:
                snapshot['attempts'][key] = {'at': at, 'status': 'provider refused request; stopped run; cache retained'}
                snapshot['last_attempt_at'] = at
                cache.save(snapshot)
                break
            except (FeedError, KeyError, ValueError, TypeError, OSError):
                snapshot['attempts'][key] = {'at': at, 'status': 'provider/transport/data error; retained prior observation'}
        snapshot['last_attempt_at'] = at
        cache.save(snapshot)
    snapshot.pop('collector_status', None)
    cache.save(snapshot)
    return snapshot


def handler_for(path):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/api/market':
                cache = Cache(path)
                try:
                    body = json.dumps(cache.get()).encode()
                finally:
                    cache.db.close()
                content = 'application/json'
            elif self.path == '/':
                body = (ROOT / 'dashboard.html').read_bytes()
                content = 'text/html; charset=utf-8'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', content)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        def log_message(self, *_):
            pass
    return Handler


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serve', action='store_true', help='Start collector loop and local dashboard')
    parser.add_argument('--refresh-seconds', type=int, default=21600)
    parser.add_argument('--daily-budget', type=int, default=12)
    parser.add_argument('--port', type=int, default=8090)
    parser.add_argument('--cache', type=Path, default=Path.home()/'.gold-journal'/'alpha-vantage.sqlite3')
    args = parser.parse_args()
    if args.refresh_seconds < 60 or args.daily_budget < 1:
        parser.error('Refresh must be >=60 seconds and daily budget >=1. Increase only with verified entitlements.')
    if not os.environ.get('ALPHA_VANTAGE_API_KEY'):
        parser.error('Set ALPHA_VANTAGE_API_KEY privately in the collector environment; ChatGPT OAuth is not inherited.')
    def run():
        cache = Cache(args.cache)
        try:
            with MCP() as client:
                result = collect(cache, client, args.daily_budget, args.refresh_seconds)
                print(json.dumps({'last_attempt_at': result.get('last_attempt_at'), 'attempts': result['attempts']}), flush=True)
        except Exception:
            # Do not log exception bodies, URLs, keys or raw provider responses.
            result = cache.get()
            result['collector_status'] = {'at': utcnow(), 'status': 'MCP startup/connection failed; cache retained'}
            cache.save(result)
            print('MCP startup/connection failed; cache retained.', flush=True)
        finally:
            cache.db.close()
    if not args.serve:
        run()
        return
    stop = threading.Event()
    def loop():
        while not stop.is_set():
            run()
            stop.wait(args.refresh_seconds)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler_for(args.cache))
    print(f'Dashboard: http://127.0.0.1:{args.port} (local only; provider refresh {args.refresh_seconds}s)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()


if __name__ == '__main__':
    main()
