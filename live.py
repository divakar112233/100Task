from flask import Flask, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Streaming Platform</title>
    <style>
        body{
            font-family:Arial;
            background:#111;
            color:white;
            text-align:center;
            padding:20px;
        }
        video{
            width:80%;
            max-width:800px;
            border:3px solid white;
            border-radius:10px;
        }
        button{
            padding:10px 20px;
            margin:10px;
            font-size:18px;
        }
    </style>
</head>
<body>

<h1>🔴 Live Streaming Platform</h1>

<video id="video" autoplay muted></video>

<br>

<button onclick="startStream()">Start Stream</button>

<script>
async function startStream(){
    try{
        const stream = await navigator.mediaDevices.getUserMedia({
            video:true,
            audio:true
        });

        document.getElementById("video").srcObject = stream;
    }
    catch(err){
        alert("Camera/Microphone access denied!");
    }
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True)