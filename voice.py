from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Voice Assistant</title>
    <style>
        body{
            font-family: Arial;
            text-align:center;
            background:#1e1e1e;
            color:white;
            margin-top:50px;
        }
        input{
            width:300px;
            padding:10px;
            border-radius:5px;
            border:none;
        }
        button{
            padding:10px 20px;
            margin:5px;
            border:none;
            border-radius:5px;
            cursor:pointer;
        }
        #response{
            margin-top:20px;
            font-size:20px;
            color:lightgreen;
        }
    </style>
</head>
<body>

<h1>🎤 AI Voice Assistant</h1>

<input type="text" id="message" placeholder="Ask something...">
<br><br>

<button onclick="sendMessage()">Send</button>
<button onclick="startVoice()">Speak</button>

<div id="response"></div>

<script>
function sendMessage(){
    let msg = document.getElementById("message").value;

    fetch("/ask",{
        method:"POST",
        headers:{
            "Content-Type":"application/x-www-form-urlencoded"
        },
        body:"message="+encodeURIComponent(msg)
    })
    .then(res=>res.json())
    .then(data=>{
        document.getElementById("response").innerHTML=data.response;

        let speech = new SpeechSynthesisUtterance(data.response);
        speechSynthesis.speak(speech);
    });
}

function startVoice(){
    let recognition = new(window.SpeechRecognition ||
                           window.webkitSpeechRecognition)();

    recognition.start();

    recognition.onresult = function(event){
        document.getElementById("message").value =
        event.results[0][0].transcript;

        sendMessage();
    };
}
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    msg = request.form["message"].lower()

    if "hello" in msg:
        reply = "Hello! How can I help you?"
    elif "time" in msg:
        reply = datetime.now().strftime("Current time is %I:%M %p")
    elif "date" in msg:
        reply = datetime.now().strftime("Today is %d %B %Y")
    elif "your name" in msg:
        reply = "I am your AI Voice Assistant."
    else:
        reply = "Sorry, I don't understand that."

    return {"response": reply}

if __name__ == "__main__":
    app.run(debug=True)