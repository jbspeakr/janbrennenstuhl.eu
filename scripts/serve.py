#!/usr/bin/env python3
"""Serve the verified build locally like the edge does: real 404s, correct MIME types,
and Markdown twins for requests that prefer text/markdown (see edge/negotiate.ts)."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import os
import sys

os.chdir(Path(__file__).resolve().parents[1] / 'public')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


def prefers_markdown(accept: str) -> bool:
    ranked = []
    for part in accept.split(','):
        media, *params = [p.strip() for p in part.split(';')]
        q = next((float(p[2:]) for p in params if p.startswith('q=')), 1.0)
        ranked.append((q, media))
    best = {m: q for q, m in ranked}
    return best.get('text/markdown', 0) > 0 and best.get('text/markdown', 0) >= max(best.get('text/html', 0), best.get('*/*', 0) if 'text/html' not in best else 0)


class Handler(SimpleHTTPRequestHandler):
    extensions_map = SimpleHTTPRequestHandler.extensions_map | {
        '.md': 'text/markdown; charset=utf-8', '.json': 'application/json; charset=utf-8',
        '.txt': 'text/plain; charset=utf-8', '.woff2': 'font/woff2', '.avif': 'image/avif'}

    def translate_path(self, path):
        local = super().translate_path(path)
        if self.path.split('?')[0].endswith('/') and prefers_markdown(self.headers.get('Accept', '')):
            twin = os.path.join(local, 'index.md')
            if os.path.isfile(twin):
                self._negotiated = True
                return twin
        return local

    def guess_type(self, path):
        if path.endswith('api-catalog'):
            return 'application/linkset+json'
        if path.endswith('feed.json'):
            return 'application/feed+json; charset=utf-8'
        return super().guess_type(path)

    def send_head(self):
        # Compress text like the CDN does, so lab measurements reflect real transfer sizes.
        path = self.translate_path(self.path.split('?')[0])
        if os.path.isdir(path):
            path = os.path.join(path, 'index.html')
        if 'gzip' in self.headers.get('Accept-Encoding', '') and os.path.isfile(path) and path.endswith(('.html', '.css', '.js', '.json', '.md', '.txt', '.xml', '.svg')):
            import gzip
            data = gzip.compress(Path(path).read_bytes())
            self.send_response(200)
            self.send_header('Content-Type', self.guess_type(path))
            self.send_header('Content-Encoding', 'gzip')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            from io import BytesIO
            return BytesIO(data)
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Vary', 'Accept')
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if code == 404:
            data = Path('404.html').read_bytes()
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(data)
        else:
            super().send_error(code, message, explain)


ThreadingHTTPServer(('127.0.0.1', PORT), Handler).serve_forever()
