#!/usr/bin/env python3
"""
serve.py -- PF Explorer release server (V5)

V5: Enforces the release-tree registry as an allowlist.
Any path not in the registry allowlist returns 404.
Quarantine/dev paths return 404.
Source viewer paths are a separate dev feature.

Usage:
    cd /mnt/d/Fundamentals/sandbox/explorer
    python3 serve.py [port]
"""

import http.server
import json
import os
import socketserver
import sys
from pathlib import Path

EXPLORER_DIR = Path(__file__).resolve().parent
FUNDAMENTALS_DIR = EXPLORER_DIR.parent.parent
REGISTRY_PATH = EXPLORER_DIR / "release_tree_registry.json"
PORT = 8080
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

# Load the registry allowlist
try:
    _REGISTRY = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    ALLOWLIST = set(_REGISTRY.get("allowlist", []))
    SOURCE_PREFIXES = _REGISTRY.get("sourceViewerPrefixes", [])
except (OSError, json.JSONDecodeError):
    print(f"ERROR: Could not load registry from {REGISTRY_PATH}", file=sys.stderr)
    ALLOWLIST = set()
    SOURCE_PREFIXES = []


class ReleaseHandler(http.server.SimpleHTTPRequestHandler):
    """V5: Only serve paths in the registry allowlist."""

    def translate_path(self, path):
        # Strip query string
        path = path.split("?")[0].split("#")[0]
        rel = path.lstrip("/")

        # Check source viewer prefixes first (dev feature)
        for prefix in SOURCE_PREFIXES:
            p = prefix.lstrip("/")
            if rel.startswith(p) or rel == p.rstrip("/"):
                return os.path.join(FUNDAMENTALS_DIR, rel)

        # V5: Check allowlist
        # Exact match
        if rel in ALLOWLIST:
            return os.path.join(EXPLORER_DIR, rel)

        # Check if it's a prefix match (for source viewer paths with subpaths)
        for entry in ALLOWLIST:
            if entry.endswith("/") and rel.startswith(entry):
                return os.path.join(EXPLORER_DIR, rel)

        # V5: Everything not in the allowlist returns 404
        # This includes dev/, quarantine/, _blocked.html, .py files, etc.
        return None  # translate_path returning None triggers 404

    def do_GET(self):
        path = self.translate_path(self.path)
        if path is None or not os.path.isfile(path):
            self.send_error(404, "Not in release tree")
            return
        try:
            with open(path, "rb") as f:
                content = f.read()
            # Guess content type
            ext = os.path.splitext(path)[1]
            ct = {
                ".html": "text/html",
                ".js": "application/javascript",
                ".json": "application/json",
                ".css": "text/css",
                ".md": "text/markdown",
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".svg": "image/svg+xml",
                ".ico": "image/x-icon",
                ".woff": "font/woff",
                ".woff2": "font/woff2",
            }.get(ext, "application/octet-stream")
            self.send_response(200)
            self.send_header("Content-Type", ct)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except OSError:
            self.send_error(404, "File not found")

    def log_message(self, format, *args):  # noqa: A002
        msg = format % args if args else format
        if "404" in msg or "403" in msg:
            print(f"  {msg}")


try:
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), ReleaseHandler) as httpd:
        print(f"PF Explorer (V5 release server)  ->  http://localhost:{PORT}/")
        print(f"Explorer dir :  {EXPLORER_DIR}")
        print(f"Registry     :  {REGISTRY_PATH}")
        print(f"Allowlist    :  {len(ALLOWLIST)} entries")
        print(f"Ctrl-C to stop.")
        httpd.serve_forever()
except OSError as e:
    if e.errno in (10048, 98):
        print(f"ERROR: Port {PORT} is already in use.")
    else:
        raise
