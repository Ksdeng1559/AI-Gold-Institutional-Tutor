"""Gold Journal local app. Run beside MT5; token stays in the server environment."""
import json
import os
import sqlite3
import threading
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = 8088
ROOT = Path(__file__).resolve().parent / "www"
ALLOWED = frozenset({"get_trading_account_info", "get_trading_open_positions",
                     "get_trading_history_orders", "get_trading_history_positions",
                     "get_time_information", "get_marketwatch_symbols"})


class BridgeError(Exception):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        raise BridgeError("MT5 redirected the request; stopped.")


class Terminal:
    def __init__(self, token):
        self.token, self.session, self.version, self.seq = token, None, "2025-03-26", 0
        self.lock = threading.Lock()
        self.opener = urllib.request.build_opener(NoRedirect)

    def rpc(self, method, params=None, notification=False):
        if not self.token:
            raise BridgeError("MT5_MCP_TOKEN is not configured on this local service.")
        self.seq += 1
        message = {"jsonrpc": "2.0", "method": method}
        if not notification:
            message["id"] = self.seq
        if params is not None:
            message["params"] = params
        headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json",
                   "Accept": "application/json, text/event-stream", "MCP-Protocol-Version": self.version}
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request("http://127.0.0.1:22346/mcp", data=json.dumps(message).encode(), headers=headers)
        try:
            with self.opener.open(req, timeout=25) as response:
                self.session = response.headers.get("Mcp-Session-Id", self.session)
                if notification or response.status == 202:
                    return {}
                if "text/event-stream" in response.headers.get("Content-Type", ""):
                    parts, size, payload = [], 0, None
                    for raw in response:
                        size += len(raw)
                        if size > 8_000_000:
                            raise BridgeError("MT5 response too large; narrow the history range.")
                        line = raw.decode("utf-8").rstrip("\r\n")
                        if line.startswith("data:"):
                            parts.append(line[5:].lstrip())
                        elif not line and parts:
                            item = json.loads("\n".join(parts))
                            parts = []
                            if item.get("id") == message.get("id"):
                                payload = item
                                break
                    if payload is None:
                        raise BridgeError("MT5 stream ended without a response.")
                else:
                    raw = response.read(8_000_001)
                    if len(raw) > 8_000_000:
                        raise BridgeError("MT5 response too large; narrow the history range.")
                    payload = json.loads(raw)
        except urllib.error.HTTPError as error:
            self.session = None
            raise BridgeError(f"MT5 returned HTTP {error.code}. Check terminal, token and permissions; reconnect.") from None
        except (urllib.error.URLError, OSError, ValueError):
            self.session = None
            raise BridgeError("Cannot read MT5. Keep the terminal running on this PC and verify its MCP settings.") from None
        if not isinstance(payload, dict) or payload.get("id") != message.get("id"):
            raise BridgeError("Invalid MT5 protocol response.")
        if "error" in payload:
            raise BridgeError("MT5 rejected this read. Inspect the discovered schema and supplied arguments.")
        return payload.get("result", {})

    def connect(self):
        self.session = None
        result = self.rpc("initialize", {"protocolVersion": self.version, "capabilities": {},
                                        "clientInfo": {"name": "gold-journal-read-only", "version": "0.1.0"}})
        self.version = result.get("protocolVersion", self.version)
        self.rpc("notifications/initialized", notification=True)

    def tools(self):
        with self.lock:
            self.connect()
            tools, cursor = [], None
            for _ in range(10):
                result = self.rpc("tools/list", {"cursor": cursor} if cursor else {})
                tools.extend(t for t in result.get("tools", []) if t.get("name") in ALLOWED)
                cursor = result.get("nextCursor")
                if not cursor:
                    return tools
            raise BridgeError("Tool list pagination incomplete.")

    def call(self, name, arguments):
        if name not in ALLOWED or not isinstance(arguments, dict):
            raise BridgeError("Only allowlisted data reads with object arguments are accepted.")
        with self.lock:
            if not self.session:
                self.connect()
            result = self.rpc("tools/call", {"name": name, "arguments": arguments})
            if result.get("isError"):
                raise BridgeError("MT5 tool reported an error. Check its schema, history range and permissions.")
            return result


def scrub(value, token):
    if isinstance(value, str):
        return value.replace(token, "[redacted]") if token else value
    if isinstance(value, dict):
        return {k: scrub(v, token) for k, v in value.items() if k.lower() not in ("api_key", "api_token", "password", "authorization")}
    if isinstance(value, list):
        return [scrub(v, token) for v in value]
    return value


def save_review(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY, created TEXT, payload TEXT)")
        cursor = db.execute("INSERT INTO reviews(created,payload) VALUES(?,?)",
                            (datetime.now(timezone.utc).isoformat(), json.dumps(body)))
        return cursor.lastrowid


def handler(terminal, database):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def reply(self, status, value):
            data = json.dumps(scrub(value, terminal.token)).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)

        def permitted(self):
            origins = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}
            return (self.headers.get("Host") in {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}
                    and self.headers.get("Origin", f"http://{self.headers.get('Host')}") in origins)

        def do_GET(self):
            if not self.permitted():
                return self.reply(403, {"error": "Local origin required."})
            if self.path == "/api/health":
                return self.reply(200, {"mode": "local", "configured": bool(terminal.token), "read_only": True})
            if self.path == "/api/reviews":
                records = []
                if database.exists():
                    with sqlite3.connect(database) as db:
                        records = [{"id": row[0], "created": row[1], "review": json.loads(row[2])} for row in
                                   db.execute("SELECT id,created,payload FROM reviews ORDER BY id DESC LIMIT 30")]
                return self.reply(200, {"records": records})
            assets = {"/": "index.html", "/journal.html": "index.html", "/journal.js": "journal.js", "/journal.css": "journal.css"}
            name = assets.get(self.path.split("?")[0])
            if not name:
                return self.reply(404, {"error": "Not found."})
            data = (ROOT / name).read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", {"html": "text/html; charset=utf-8", "js": "text/javascript", "css": "text/css"}[name.rsplit(".", 1)[1]])
            self.send_header("Content-Security-Policy", "default-src 'self'; connect-src 'self'; script-src 'self'; style-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(data)

        def do_POST(self):
            if not self.permitted() or self.headers.get("X-Journal-Request") != "1":
                return self.reply(403, {"error": "Local journal request required."})
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length < 0 or length > 2_000_000:
                    return self.reply(413, {"error": "Request too large."})
                body = json.loads(self.rfile.read(length) or b"{}")
                if not isinstance(body, dict):
                    raise ValueError()
                if self.path == "/api/mt5/tools":
                    return self.reply(200, {"tools": terminal.tools(), "retrieved_at": datetime.now(timezone.utc).isoformat()})
                if self.path == "/api/mt5/call":
                    result = terminal.call(body.get("name"), body.get("arguments", {}))
                    return self.reply(200, {"result": result, "tool": body.get("name"), "retrieved_at": datetime.now(timezone.utc).isoformat()})
                if self.path == "/api/reviews":
                    if not isinstance(body.get("notes"), str) or not isinstance(body.get("date"), str):
                        raise ValueError()
                    review_id = save_review(database, scrub(body, terminal.token))
                    return self.reply(200, {"id": review_id, "saved": True})
                return self.reply(404, {"error": "Not found."})
            except BridgeError as error:
                self.reply(502, {"error": str(error)})
            except (ValueError, TypeError):
                self.reply(400, {"error": "Invalid request data."})
            except Exception:
                self.reply(500, {"error": "Local service error. No trade action was attempted."})
    return Handler


if __name__ == "__main__":
    token = os.environ.get("MT5_MCP_TOKEN", "")
    database = Path(os.environ.get("GOLD_JOURNAL_DB", str(Path.home() / ".gold-journal" / "journal.sqlite3")))
    server = ThreadingHTTPServer(("127.0.0.1", PORT), handler(Terminal(token), database))
    print(f"Gold Journal: http://127.0.0.1:{PORT} — read-only MT5 data access. Ctrl+C to stop.")
    server.serve_forever()
