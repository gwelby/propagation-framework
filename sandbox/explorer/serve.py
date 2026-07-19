#!/usr/bin/env python3
"""
serve.py -- PF Explorer release server (V5.1)

V5.1: Release server serves ONLY exact normalized release-tree paths.
Source-viewer prefixes are removed from the release server entirely.
Any path not in the registry allowlist returns 404.
Traversal attempts (../) are canonicalized and rejected.

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
except (OSError, json.JSONDecodeError):
    print(f"ERROR: Could not load registry from {REGISTRY_PATH}", file=sys.stderr)
    ALLOWLIST = set()


class ReleaseHandler(http.server.SimpleHTTPRequestHandler):
    """V5.1: Only serve exact normalized paths in the registry allowlist."""

    def translate_path(self, path):
        # Strip query string and fragment
        path = path.split("?")[0].split("#")[0]
        rel = path.lstrip("/")

        # V5.1: Canonicalize to reject traversal (../) attempts
        # os.path.normpath collapses ../ sequences
        rel_norm = os.path.normpath(rel)
        # If normalization changed the path (traversal was attempted), reject
        if rel_norm != rel and rel_norm.replace("\\", "/") != rel:
            return None  # traversal attempt -> 404
        # Reject any path that still contains .. after normalization
        if ".." in rel_norm.split("/"):
            return None

        # V5.1: Check exact allowlist match
        if rel_norm in ALLOWLIST:
            candidate = (EXPLORER_DIR / rel_norm).resolve()
            # Containment check: resolved path must be under EXPLORER_DIR
            try:
                candidate.relative_to(EXPLORER_DIR)
            except ValueError:
                return None  # escaped explorer dir -> 404
            return str(candidate)

        # V5.1: Check prefix match (for directory entries ending with /)
        for entry in ALLOWLIST:
            if entry.endswith("/") and rel_norm.startswith(entry):
                candidate = (EXPLORER_DIR / rel_norm).resolve()
                try:
                    candidate.relative_to(EXPLORER_DIR)
                except ValueError:
                    return None
                return str(candidate)

        # V5.1: Everything not in the allowlist returns 404
        # This includes dev/, quarantine/, _blocked.html, .py files,
        # source-viewer prefixes, and traversal attempts.
        return None

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
        print(f"PF Explorer (V5.1 release server)  ->  http://localhost:{PORT}/")
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
