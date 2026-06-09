from flask import Flask, render_template_string, request, jsonify, send_from_directory
import os
import uuid
from werkzeug.utils import secure_filename
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeTube • Upload</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.6.0/css/all.min.css">
    <style>
        .upload-zone { transition: all 0.3s; }
        .upload-zone.dragover { background-color: #1e2937; border-color: #22d3ee; }
        video { max-height: 180px; }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-200">
    <div class="max-w-7xl mx-auto p-8">
        <div class="flex justify-between items-center mb-10">
            <h1 class="text-5xl font-bold tracking-tighter">
                <span class="text-cyan-400">Vibe</span>Tube
            </h1>
            <div class="text-sm text-zinc-500">Single File • Local Server</div>
        </div>

        <!-- Upload Area -->
        <div id="uploadZone" 
             class="upload-zone border-4 border-dashed border-zinc-700 rounded-3xl p-20 text-center mb-12 hover:border-cyan-400 cursor-pointer"
             onclick="document.getElementById('fileInput').click()">
            <i class="fas fa-cloud-upload-alt text-7xl text-zinc-500 mb-6"></i>
            <h2 class="text-3xl font-semibold mb-3">Drop video here or click to upload</h2>
            <p class="text-zinc-400 mb-8">MP4, MOV, AVI, MKV, WEBM • Up to 500MB</p>
            <input type="file" id="fileInput" accept="video/*" class="hidden" onchange="uploadFile(event)">
        </div>

        <div id="status" class="hidden mb-8 p-5 rounded-2xl"></div>

        <!-- Video Gallery -->
        <h2 class="text-2xl font-semibold mb-6 flex items-center gap-3">
            <i class="fas fa-film text-cyan-400"></i> Your Uploaded Videos
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6" id="videoGrid">
            {% for video in videos %}
            <div class="bg-zinc-900 rounded-2xl overflow-hidden border border-zinc-800">
                <div class="relative">
                    <video src="/uploads/{{ video.filename }}" class="w-full" controls></video>
                </div>
                <div class="p-4">
                    <h3 class="font-medium text-lg">{{ video.name }}</h3>
                    <p class="text-xs text-zinc-500">{{ video.date }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        function showStatus(msg, type) {
            const status = document.getElementById('status');
            status.className = `mb-8 p-5 rounded-2xl ${type === 'success' ? 'bg-green-900 text-green-300' : 'bg-red-900 text-red-300'}`;
            status.textContent = msg;
            status.classList.remove('hidden');
            setTimeout(() => status.classList.add('hidden'), 5000);
        }

        async function uploadFile(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('video', file);

            const status = document.getElementById('status');
            status.className = "mb-8 p-5 rounded-2xl bg-zinc-900";
            status.textContent = `Uploading ${file.name}...`;
            status.classList.remove('hidden');

            try {
                const res = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();

                if (data.success) {
                    showStatus('✅ Video uploaded successfully!', 'success');
                    setTimeout(() => location.reload(), 1200);
                } else {
                    showStatus('❌ ' + (data.error || 'Upload failed'), 'error');
                }
            } catch (err) {
                showStatus('❌ Upload failed', 'error');
            }
        }

        // Drag and Drop
        const dropZone = document.getElementById('uploadZone');
        dropZone.addEventListener('dragover', e => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });
        dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
        dropZone.addEventListener('drop', e => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                const file = e.dataTransfer.files[0];
                const fakeEvent = { target: { files: [file] } };
                uploadFile(fakeEvent);
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    videos = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(file):
            videos.append({
                'filename': file,
                'name': file.split('_', 1)[-1].rsplit('.', 1)[0].replace('-', ' ').title(),
                'date': datetime.datetime.fromtimestamp(
                    os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], file))
                ).strftime('%d %b %Y')
            })
    videos.reverse()  # Latest first
    return render_template_string(HTML, videos=videos)

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'success': True, 'filename': filename})
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    print("🚀 VibeTube Video Upload Platform Started!")
    print("🌐 Open: http://127.0.0.1:5000")
    app.run(debug=True)