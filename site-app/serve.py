#!/usr/bin/env python3
"""Static server that resolves extensionless URLs, matching Cloudflare Workers.

The generator emits links without `.html` (`/l1/lesson/week-01`) while the files on disk
keep the extension. Workers' static-asset handling resolves that automatically; Python's
stock `http.server` does not, so local serving would 404 on every link.

Resolution order for a request path P, first hit wins:
    P                     (exact file)
    P.html
    P/index.html
Binds to localhost only. Nothing is published.
"""

from __future__ import annotations

import functools
import http.server
import os
import socketserver
import sys
from pathlib import Path


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".svg": "image/svg+xml",
        ".json": "application/json",
        ".js": "text/javascript",
        ".css": "text/css",
    }

    def translate_path(self, path: str) -> str:
        real = super().translate_path(path)
        p = Path(real)
        if p.is_file() or p.is_dir() and (p / "index.html").is_file():
            return real
        for candidate in (p.with_name(p.name + ".html"), p / "index.html"):
            if candidate.is_file():
                return str(candidate)
        return real

    def end_headers(self):
        # dev server: never cache, so a rebuild is visible on reload
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        if "404" in (fmt % args):
            sys.stderr.write("  404  %s\n" % (args[0] if args else ""))


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    root = Path(__file__).resolve().parent / "dist"
    if not root.is_dir():
        sys.exit("No dist/ — run:  python3 site-app/build.py --clean")
    os.chdir(root)
    handler = functools.partial(Handler, directory=str(root))

    class Server(socketserver.ThreadingTCPServer):
        allow_reuse_address = True
        daemon_threads = True

    with Server(("127.0.0.1", port), handler) as httpd:
        print(f"  serving {root} on http://localhost:{port}/")
        print("  extensionless URLs resolved (P -> P.html -> P/index.html)")
        print("  Ctrl-C to stop. Local only — nothing is published.\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
