from flask import Flask, render_template_string, request, session, redirect
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.secret_key = "notification-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

# Store notifications
notifications = []

# Simple HTML
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Notifications</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
</head>
<body class="bg-gray-100">
    <div class="max-w-2xl mx-auto mt-8 bg-white shadow-xl rounded-2xl overflow-hidden">
        
        <!-- Header -->
        <div class="bg-indigo-600 text-white p-5 flex justify-between items-center">
            <h1 class="text-2xl font-bold">🛎️ Real-Time Notifications</h1>
            <span id="username" class="font-medium"></span>
        </div>

        <!-- Send Notification -->
        <div class="p-5 border-b">
            <form id="send-form" class="flex gap-3">
                <input id="title" type="text" placeholder="Notification Title" 
                       class="flex-1 border rounded-lg px-4 py-3 focus:outline-none">
                <button type="submit" 
                        class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-medium">
                    Send
                </button>
            </form>
        </div>

        <!-- Notifications List -->
        <div id="notif-list" class="divide-y max-h-[70vh] overflow-y-auto"></div>
    </div>

<script>
    const socket = io();
    const username = "{{ username }}";
    document.getElementById('username').textContent = username;

    // Receive new notification
    socket.on('new notification', function(notif) {
        addNotification(notif);
    });

    function addNotification(notif) {
        const div = document.createElement('div');
        div.className = "p-5 hover:bg-gray-50 transition";
        div.innerHTML = `
            <div class="flex justify-between">
                <div>
                    <span class="font-semibold text-indigo-700">${notif.title}</span>
                    <p class="text-gray-600 mt-1">${notif.message}</p>
                </div>
                <small class="text-gray-400">${notif.time}</small>
            </div>
            <small class="text-gray-500">From: ${notif.sender}</small>
        `;
        document.getElementById('notif-list').prepend(div);
    }

    // Send notification
    document.getElementById('send-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const title = document.getElementById('title').value.trim();
        
        if (title) {
            socket.emit('send notification', {
                title: title,
                message: "New update available",
                sender: username
            });
            document.getElementById('title').value = '';
        }
    });

    // Load existing notifications
    socket.on('load notifications', function(data) {
        data.forEach(notif => addNotification(notif));
    });
</script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('username', 'User').strip()
        if name:
            session['username'] = name
            return redirect('/notifications')
    
    return """
    <div class="max-w-md mx-auto mt-20 bg-white p-8 rounded-2xl shadow text-center">
        <h1 class="text-3xl font-bold mb-6">Real-Time Notifications</h1>
        <form method="post">
            <input type="text" name="username" placeholder="Enter your name" 
                   class="w-full p-4 border rounded-xl mb-6 text-lg" required>
            <button type="submit" class="w-full bg-indigo-600 text-white py-4 rounded-xl font-bold text-lg">
                Enter Notification System
            </button>
        </form>
    </div>
    """

@app.route('/notifications')
def notifications():
    if 'username' not in session:
        return redirect('/')
    return render_template_string(HTML, username=session['username'])

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    emit('load notifications', notifications)

@socketio.on('send notification')
def handle_notification(data):
    notif = {
        'title': data['title'],
        'message': data.get('message', 'New notification'),
        'sender': data['sender'],
        'time': datetime.now().strftime("%H:%M")
    }
    notifications.append(notif)
    emit('new notification', notif, broadcast=True)

if __name__ == '__main__':
    print("🚀 Real-Time Notification System Started")
    print("Visit → http://127.0.0.1:5000")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)