from flask import Flask, request, render_template_string, redirect, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Cloud File Storage</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    padding:20px;
}
.container{
    max-width:800px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:10px;
}
.file{
    padding:10px;
    border-bottom:1px solid #ddd;
}
button{
    padding:10px 20px;
}
</style>
</head>
<body>

<div class="container">
<h1>☁️ Cloud File Storage System</h1>

<form method="POST" enctype="multipart/form-data">
<input type="file" name="file" required>
<button type="submit">Upload</button>
</form>

<hr>

<h2>Stored Files</h2>

{% for file in files %}
<div class="file">
    {{ file }}
    <a href="/download/{{ file }}">Download</a>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        uploaded_file = request.files["file"]

        if uploaded_file.filename:
            uploaded_file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    uploaded_file.filename
                )
            )

        return redirect("/")

    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(
        HTML,
        files=files
    )

@app.route("/download/<filename>")
def download(filename):
    return send_from_directory(
        UPLOAD_FOLDER,
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)