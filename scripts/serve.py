#!/usr/bin/env python3
"""Serve verified output locally, including the real 404 page and Markdown MIME."""
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import os
os.chdir(Path(__file__).resolve().parents[1]/'public')
class Handler(SimpleHTTPRequestHandler):
    extensions_map=SimpleHTTPRequestHandler.extensions_map | {'.md':'text/markdown; charset=utf-8','.json':'application/json; charset=utf-8'}
    def end_headers(self):
        self.send_header('Cache-Control','no-cache');super().end_headers()
    def send_error(self,code,message=None,explain=None):
        if code==404:
            data=Path('404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
            if self.command!='HEAD':self.wfile.write(data)
        else:super().send_error(code,message,explain)
ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
