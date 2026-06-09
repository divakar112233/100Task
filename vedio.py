import sys
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os

def download_youtube(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    try:
        cmd = [
            'yt-dlp',
            '-f', 'bestvideo+bestaudio/best',  # Best quality
            '--merge-output-format', 'mp4',
            '-o', f'{output_dir}/%(title)s.%(ext)s',
            '--no-playlist',  # Download single video
            url
        ]
        print("Downloading... Please wait.")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Try to find the downloaded file
            for file in os.listdir(output_dir):
                if file.endswith(('.mp4', '.webm', '.mkv')):
                    return os.path.join(output_dir, file)
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/download?'):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            url = params.get('url', [None])[0]
            
            if url:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<h2>Downloading... Check terminal for progress.</h2>")
                self.wfile.write(b"<p>It may take a while for long videos.</p>")
                
                file_path = download_youtube(url)
                if file_path:
                    print(f"✅ Download complete: {file_path}")
                else:
                    print("❌ Download failed")
                return

        # Main Page
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """<!DOCTYPE html>
        <html>
        <head>
            <title>YouTube Video Downloader</title>
            <style>
                body { font-family: Arial; margin: 40px; background: #f0f0f0; text-align: center; }
                input[type=text] { width: 700px; padding: 15px; font-size: 18px; }
                input[type=submit] { padding: 15px 40px; font-size: 18px; background: #ff0000; color: white; border: none; cursor: pointer; }
                h1 { color: #ff0000; }
            </style>
        </head>
        <body>
            <h1>📥 YouTube Video Downloader</h1>
            <form action="/download" method="get">
                <input type="text" name="url" placeholder="Paste YouTube URL here" value="https://www.youtube.com/watch?v=dQw4w9wgxcq">
                <br><br>
                <input type="submit" value="⬇️ Download Video">
            </form>
            <p><strong>Supports:</strong> Videos, Shorts, Playlists (remove --no-playlist if needed)</p>
        </body>
        </html>"""
        self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        file_path = download_youtube(url)
        if file_path:
            print(f"✅ Saved to: {file_path}")
        else:
            print("❌ Failed to download")
    else:
        server = HTTPServer(('localhost', 8080), Handler)
        print("🚀 Server running at http://localhost:8080")
        print("Open this link in your browser")
        server.serve_forever()