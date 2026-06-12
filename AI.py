from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Chatbot</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg,#667eea,#764ba2);
            margin:0;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
        }

        .chat-container{
            width:500px;
            background:white;
            border-radius:15px;
            box-shadow:0 0 20px rgba(0,0,0,0.3);
            padding:20px;
        }

        h2{
            text-align:center;
            color:#333;
        }

        .chat-box{
            height:300px;
            overflow-y:auto;
            border:1px solid #ddd;
            padding:10px;
            border-radius:10px;
            background:#f9f9f9;
        }

        .user{
            color:blue;
            margin:10px 0;
        }

        .bot{
            color:green;
            margin:10px 0;
        }

        form{
            display:flex;
            margin-top:10px;
        }

        input{
            flex:1;
            padding:10px;
            border:1px solid #ccc;
            border-radius:5px;
        }

        button{
            padding:10px 20px;
            margin-left:5px;
            background:#4CAF50;
            color:white;
            border:none;
            border-radius:5px;
            cursor:pointer;
        }

        button:hover{
            background:#45a049;
        }
    </style>
</head>
<body>

<div class="chat-container">
    <h2>🤖 AI Chatbot</h2>

    <div class="chat-box">
        {% for msg in messages %}
            <div class="{{ msg.role }}">
                <b>{{ msg.role.title() }}:</b> {{ msg.text }}
            </div>
        {% endfor %}
    </div>

    <form method="POST">
        <input type="text" name="message"
               placeholder="Type your message..." required>
        <button type="submit">Send</button>
    </form>
</div>

</body>
</html>
"""

messages = []

def chatbot_reply(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hello! How can I help you?"
    elif "hi" in user_input:
        return "Hi there!"
    elif "your name" in user_input:
        return "I am a simple AI Chatbot."
    elif "python" in user_input:
        return "Python is a popular programming language."
    elif "bye" in user_input:
        return "Goodbye! Have a nice day."
    else:
        return "Sorry, I don't understand that yet."

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_message = request.form["message"]

        messages.append({
            "role": "user",
            "text": user_message
        })

        bot_response = chatbot_reply(user_message)

        messages.append({
            "role": "bot",
            "text": bot_response
        })

    return render_template_string(
        html,
        messages=messages
    )

if __name__ == "__main__":
    app.run(debug=True)