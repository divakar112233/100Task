from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Video Call App</title>
    <style>
        body{
            text-align:center;
            font-family:Arial;
            background:#222;
            color:white;
        }
        video{
            width:45%;
            margin:10px;
            border:2px solid white;
        }
    </style>
</head>
<body>

<h1>📹 Real-Time Video Call</h1>

<video id="localVideo" autoplay muted></video>
<video id="remoteVideo" autoplay></video>

<script>
const localVideo = document.getElementById('localVideo');

navigator.mediaDevices.getUserMedia({
    video:true,
    audio:true
})
.then(stream=>{
    localVideo.srcObject = stream;
})
.catch(err=>{
    alert("Camera access denied!");
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)