from flask import Flask, render_template_string, request, session, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.secret_key = "simplechat"
socketio = SocketIO(app, cors_allowed_origins="*")

messages = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
</head>
<body class="bg-gray-100 p-6">
    <div class="max-w-md mx-auto bg-white rounded-xl shadow-lg overflow-hidden">
        <div class="bg-blue-600 p-4 text-white text-center font-bold">💬 Simple Chat</div>
        
        <div id="messages" class="h-80 p-4 overflow-y-auto"></div>
        
        <form id="form" class="p-4 border-t flex">
            <input id="input" type="text" class="flex-1 border rounded-l-lg px-4 py-3 focus:outline-none" 
                   placeholder="Type message..." autocomplete="off">
            <button type="submit" class="bg-blue-600 text-white px-6 rounded-r-lg">Send</button>
        </form>
    </div>

<script>
    const socket = io();
    const username = "{{ username }}";

    socket.on('message', (data) => {
        const div = document.createElement('div');
        div.className = 'mb-2';
        div.innerHTML = `<b>${data.username}:</b> ${data.text} <small>(${data.time})</small>`;
        document.getElementById('messages').appendChild(div);
        div.scrollIntoView();
    });

    document.getElementById('form').onsubmit = (e) => {
        e.preventDefault();
        const input = document.getElementById('input');
        if (input.value.trim()) {
            socket.emit('message', {username: username, text: input.value});
            input.value = '';
        }
    };
</script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('username', 'Guest').strip()
        if name:
            session['username'] = name
            return redirect('/chat')
    return """
    <div class="max-w-sm mx-auto mt-20 bg-white p-8 rounded shadow text-center">
        <h1 class="text-3xl font-bold mb-6">Join Chat</h1>
        <form method="post">
            <input type="text" name="username" placeholder="Your Name" class="w-full p-4 border rounded mb-4" required>
            <button type="submit" class="w-full bg-blue-600 text-white py-4 rounded font-bold">Join</button>
        </form>
    </div>
    """

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect('/')
    return render_template_string(HTML, username=session['username'])

@socketio.on('message')
def handle_msg(data):
    msg = {
        'username': data['username'],
        'text': data['text'],
        'time': datetime.now().strftime("%H:%M")
    }
    emit('message', msg, broadcast=True)

if __name__ == '__main__':
    print("🚀 Chat Started at http://127.0.0.1:5000")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)