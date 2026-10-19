import importlib.util
import io
import json
import sqlite3
import tempfile
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
from http.server import ThreadingHTTPServer

spec = importlib.util.spec_from_file_location("journal_server", Path(__file__).resolve().parents[1] / "server.py")
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class Response(io.BytesIO):
    def __init__(self, data, content_type="application/json"):
        super().__init__(data)
        self.status = 200
        self.headers = {"Content-Type": content_type, "Mcp-Session-Id": "test-session"}


class FakeMT5:
    def __init__(self, sse=False):
        self.requests = []
        self.sse = sse

    def open(self, request, timeout):
        msg = json.loads(request.data)
        self.requests.append((msg, dict(request.headers)))
        method = msg["method"]
        if method == "initialize":
            result = {"protocolVersion": "2025-03-26", "capabilities": {}, "serverInfo": {"name": "fixture"}}
        elif method == "tools/list":
            result = {"tools": [{"name": "get_trading_account_info", "inputSchema": {}}, {"name": "trade_send_market_order"}]}
        else:
            result = {"content": [{"type": "text", "text": "fixture"}]}
        payload = {"jsonrpc": "2.0", "id": msg.get("id"), "result": result}
        data = json.dumps(payload).encode()
        return Response(b"data: " + data + b"\n\n" if self.sse else data,
                        "text/event-stream" if self.sse else "application/json")


class ProtocolTests(unittest.TestCase):
    def test_json_and_sse_initialization_and_allowlist(self):
        for sse in (False, True):
            terminal = app.Terminal("private-test-token")
            terminal.opener = fake = FakeMT5(sse)
            self.assertEqual([t["name"] for t in terminal.tools()], ["get_trading_account_info"])
            terminal.call("get_trading_account_info", {})
            methods = [r[0]["method"] for r in fake.requests]
            self.assertEqual(methods, ["initialize", "notifications/initialized", "tools/list", "tools/call"])
            self.assertEqual(fake.requests[-1][1].get("Mcp-session-id"), "test-session")
            before = len(fake.requests)
            for name in ("trade_send_market_order", "trade_close_single_position", "shell", "chart_open"):
                with self.assertRaises(app.BridgeError):
                    terminal.call(name, {})
            self.assertEqual(len(fake.requests), before)

    def test_missing_secret_and_redaction(self):
        with self.assertRaises(app.BridgeError):
            app.Terminal("").tools()
        safe = app.scrub({"api_key": "hide", "text": "token=private-test-token", "nested": [{"password": "hide"}]}, "private-test-token")
        self.assertNotIn("private-test-token", json.dumps(safe))
        self.assertNotIn("password", json.dumps(safe))

    def test_redirect_block(self):
        with self.assertRaises(app.BridgeError):
            app.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.org")


class LocalHTTPTests(unittest.TestCase):
    def test_origin_checks_persistence_and_no_trade_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / "journal.sqlite3"
            terminal = app.Terminal("test-secret")
            terminal.opener = FakeMT5()
            server = ThreadingHTTPServer(("127.0.0.1", 0), app.handler(terminal, db))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            url = "http://127.0.0.1:" + str(server.server_port)
            def post(path, data, origin="http://127.0.0.1:8088", header=True):
                headers = {"Host": "127.0.0.1:8088", "Origin": origin, "Content-Type": "application/json"}
                if header:
                    headers["X-Journal-Request"] = "1"
                return urllib.request.urlopen(urllib.request.Request(url + path, data=json.dumps(data).encode(), headers=headers))
            try:
                for origin, header in (("https://evil.example", True), ("http://127.0.0.1:8088", False)):
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        post("/api/reviews", {"date": "2026-10-18", "notes": "text"}, origin, header)
                    self.assertEqual(caught.exception.code, 403)
                with post("/api/reviews", {"date": "2026-10-18", "notes": "test-secret reviewed"}) as r:
                    self.assertTrue(json.load(r)["saved"])
                with sqlite3.connect(db) as connection:
                    stored = connection.execute("SELECT payload FROM reviews").fetchone()[0]
                    self.assertNotIn("test-secret", stored)
                with self.assertRaises(urllib.error.HTTPError) as caught:
                    post("/api/mt5/call", {"name": "trade_send_market_order", "arguments": {}})
                self.assertEqual(caught.exception.code, 502)
            finally:
                server.shutdown()
                server.server_close()


if __name__ == "__main__":
    unittest.main()
