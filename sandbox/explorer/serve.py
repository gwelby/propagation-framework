#!/usr/bin/env python3
"""
serve.py -- PF Explorer dev server
Serves explorer files from this directory, AND serves Fundamentals
source files (derivations/, definitions/, etc.) for the source viewer.

Usage:
    cd /mnt/d/Fundamentals/sandbox/explorer
    python3 serve.py
    # then open http://localhost:8080/
"""

import http.server, os, socketserver, sys

EXPLORER_DIR    = os.path.dirname(os.path.abspath(__file__))
FUNDAMENTALS_DIR = os.path.abspath(os.path.join(EXPLORER_DIR, '..', '..'))
PORT = 8080
if len(sys.argv) > 1:
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        pass

# Directories in Fundamentals root that source-viewer may fetch
SOURCE_PREFIXES = (
    '/derivations/', '/definitions/', '/papers/', '/verification/',
    '/sandbox_results', '/CLAIMS', '/ACTIVE_ISSUES',
)

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve source files from Fundamentals root
        for prefix in SOURCE_PREFIXES:
            if path.startswith(prefix) or path == prefix.rstrip('/'):
                rel = path.lstrip('/')
                return os.path.join(FUNDAMENTALS_DIR, rel)
        # Everything else from the explorer directory
        rel = path.lstrip('/')
        return os.path.join(EXPLORER_DIR, rel)

    def log_message(self, format, *args):  # noqa: A002
        # Only print 404s -- suppress noisy 200s
        msg = format % args if args else format
        if '404' in msg:
            print(f'  404  {msg}')

try:
    with socketserver.ThreadingTCPServer(('', PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        print(f'PF Explorer  ->  http://localhost:{PORT}/')
        print(f'Explorer dir :  {EXPLORER_DIR}')
        print(f'Sources root :  {FUNDAMENTALS_DIR}')
        print(f'Ctrl-C to stop.')
        httpd.serve_forever()
except OSError as e:
    if e.errno == 10048: # Address already in use
        print(f"ERROR: Port {PORT} is already in use.")
    else:
        raise e
