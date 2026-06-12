from flask import Flask, request, render_template_string, redirect, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "drive_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Google Drive Clone</title>
<style>
body{
    font-family:Arial;
    background:#f5f5f5;
    margin:0;
}
.header{
    background:#4285F4;
    color:white;
    padding:15px;
    text-align:center;
}
.container{
    width:80%;
    margin:auto;
    padding:20px;
}
.card{
    background:white;
    padding:15px;
    margin:10px 0;
    border-radius:10px;
    box-shadow:0 0 5px #ccc;
}
button{
    padding:8px 15px;
    background:#4285F4;
    color:white;
    border:none;
    cursor:pointer;
}
</style>
</head>
<body>

<div class="header">
    <h1>☁ Google Drive Clone</h1>
</div>

<div class="container">

<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" required>
    <button type="submit">Upload</button>
</form>

<hr>

<h2>My Files</h2>

{% for file in files %}
<div class="card">
    <strong>{{ file }}</strong><br><br>
    <a href="/download/{{ file }}">
        <button>Download</button>
    </a>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file = request.files["file"]

        if file.filename:
            file.save(
                os.path.join(
                    UPLOAD_FOLDER,
                    file.filename
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