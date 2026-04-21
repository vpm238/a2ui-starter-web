#!/usr/bin/env python3
"""Local LLM proxy for the a2ui-starter-web demo.

Same API shape as the Cloudflare Worker version (`llm-proxy.js`) but runs on
your laptop with zero account setup. Good for demos, local dev, and screen-
sharing without exposing your API key in the browser.

Usage:
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 proxy/local-proxy.py            # listens on :8787

Then in web/index.html, set:
    window.A2UI_PROXY_URL = 'http://localhost:8787';

Requires Python 3.9+. Standard library only (urllib + http.server). No pip install.
"""

import http.server
import json
import os
import socketserver
import sys
import urllib.request
import urllib.error

PORT = int(os.environ.get("PORT", "8787"))
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"


class ProxyHandler(http.server.BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, anthropic-version")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        if self.path != "/v1/messages":
            self.send_response(404); self._cors(); self.end_headers()
            self.wfile.write(b'{"error":"not found"}')
            return

        if not API_KEY:
            self.send_response(500); self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error":"ANTHROPIC_API_KEY env var is not set"}')
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)

        req = urllib.request.Request(
            ANTHROPIC_URL,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                self.send_response(resp.status)
                self._cors()
                self.send_header("Content-Type", resp.headers.get("Content-Type", "text/event-stream"))
                self.send_header("Cache-Control", "no-cache")
                self.end_headers()
                # Stream the upstream SSE body to the client untouched.
                while True:
                    chunk = resp.read(1024)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    try:
                        self.wfile.flush()
                    except BrokenPipeError:
                        return
        except urllib.error.HTTPError as e:
            self.send_response(e.code); self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502); self._cors()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, fmt, *args):
        # Cleaner one-liner log: "POST /v1/messages → 200"
        sys.stderr.write(f"{self.command} {self.path} → {fmt % args}\n".replace("\"", ""))


class ReusableTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> None:
    if not API_KEY:
        print("WARNING: ANTHROPIC_API_KEY not set; requests will 500.", file=sys.stderr)
    print(f"a2ui local LLM proxy listening on http://localhost:{PORT}", file=sys.stderr)
    print(f"In web/index.html, set:  window.A2UI_PROXY_URL = 'http://localhost:{PORT}'", file=sys.stderr)
    with ReusableTCPServer(("127.0.0.1", PORT), ProxyHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nbye", file=sys.stderr)


if __name__ == "__main__":
    main()
