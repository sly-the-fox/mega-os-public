#!/usr/bin/env python3
"""Minimal receiver for LinkedIn profile captures from the Outreach Capture extension.

Binds to 127.0.0.1:7799 (or OUTREACH_PORT env var).
Saves captured profiles as JSON files. No dependencies beyond stdlib.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

PORT = int(os.environ.get("OUTREACH_PORT", 7799))
CAPTURES_DIR = os.environ.get(
    "OUTREACH_CAPTURES_DIR",
    str(Path(__file__).resolve().parent.parent.parent.parent / "business" / "network" / "captures")
)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        for k, v in CORS_HEADERS.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_OPTIONS(self):
        self._send(200, {})

    def do_GET(self):
        if self.path == "/health":
            pending = sum(
                1 for f in Path(CAPTURES_DIR).glob("*.json")
                if not json.loads(f.read_text()).get("processed", False)
            ) if Path(CAPTURES_DIR).exists() else 0
            self._send(200, {"status": "ok", "captures_dir": CAPTURES_DIR, "pending": pending})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/capture":
            self._send(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, ValueError):
            self._send(400, {"success": False, "error": "invalid JSON"})
            return

        text = (data.get("text") or "").strip()
        name = (data.get("name") or "").strip()
        url = (data.get("url") or "").strip()

        if not text:
            self._send(400, {"success": False, "error": "no profile text provided"})
            return
        if not name:
            self._send(400, {"success": False, "error": "no profile name provided"})
            return

        Path(CAPTURES_DIR).mkdir(parents=True, exist_ok=True)

        safe_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_{timestamp}.json"

        capture = {
            "name": name,
            "url": url,
            "text": text,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "processed": False,
        }

        filepath = Path(CAPTURES_DIR) / filename
        filepath.write_text(json.dumps(capture, indent=2))

        print(f"Captured: {filename} ({len(text)} chars)")
        self._send(200, {"success": True, "filename": filename})

    def log_message(self, format, *args):
        print(f"[receiver] {args[0]}" if args else "")


if __name__ == "__main__":
    print(f"Outreach receiver starting on 127.0.0.1:{PORT}")
    print(f"Captures dir: {CAPTURES_DIR}")
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.shutdown()
