import sys
import subprocess
import os
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

def take_screenshot(url, output_file=None):
    if output_file is None:
        output_file = f"screenshot_{uuid.uuid4().hex[:8]}.png"
    try:
        cmd = [
            'google-chrome',
            '--headless',
            '--no-sandbox',
            '--disable-gpu',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--window-size=1920,1080',
            '--screenshot=' + output_file,
            url
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 1000:
            return output_file, None
        else:
            error_msg = result.stderr or result.stdout or "Unknown error"
            return None, error_msg
    except Exception as e:
        return None, str(e)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/screenshot?'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            url = params.get('url', [None])[0]
            if url:
                screenshot, error = take_screenshot(url)
                if screenshot:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/png')
                    self.end_headers()
                    with open(screenshot, 'rb') as f:
                        self.wfile.write(f.read())
                    os.remove(screenshot)
                    return
                else:
                    self.send_response(500)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"<h2>Error:</h2><pre>{error}</pre>".encode())
                    return

        # Main page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """<html>
        <head><title>URL Screenshot Generator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }
            h1 { color: #333; }
            input[type=text] { width: 600px; padding: 12px; font-size: 18px; border: 1px solid #ccc; }
            input[type=submit] { padding: 12px 30px; font-size: 18px; background: #0066cc; color: white; border: none; cursor: pointer; }
        </style>
        </head>
        <body>
        <h1>🌐 URL Screenshot Generator</h1>
        <form action="/screenshot" method="get">
            <input type="text" name="url" placeholder="https://example.com" value="https://httpbin.org/html" style="margin-bottom: 10px;">
            <br>
            <input type="submit" value="📸 Take Screenshot">
        </form>
        <p><strong>Try these test URLs:</strong> https://httpbin.org/html | https://picsum.photos</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        screenshot, error = take_screenshot(url)
        if screenshot:
            print(f"✅ Screenshot saved: {screenshot}")
        else:
            print(f"❌ Error: {error}")
    else:
        server = HTTPServer(('0.0.0.0', 8080), Handler)
        print("🚀 Server started at http://localhost:8080")
        print("Open that URL in your browser")
        server.serve_forever()