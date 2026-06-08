from flask import Flask, render_template_string, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "my-super-secret-key"   # Change this later

# ====================== DATABASE (Simple List - No real DB for beginners) ======================
posts = []        # List to store all blog posts
users = {"admin": "admin123"}   # Default username: admin, password: admin123

# ====================== HTML TEMPLATE ======================
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">

<div class="max-w-4xl mx-auto p-6">

    <!-- Navigation -->
    <nav class="bg-white shadow p-4 rounded mb-8 flex justify-between">
        <a href="/" class="text-xl font-bold">🏠 My Blog</a>
        <div>
            {% if session.get('logged_in') %}
                <a href="/dashboard" class="mr-4 text-blue-600">Dashboard</a>
                <a href="/logout" class="text-red-600">Logout</a>
            {% else %}
                <a href="/login" class="text-blue-600">Login</a>
            {% endif %}
        </div>
    </nav>

    {% block content %}{% endblock %}

</div>
</body>
</html>
"""

# ====================== ROUTES ======================

@app.route('/')
def home():
    html = BASE_HTML.replace('{% block content %}{% endblock %}', '''
    <h1 class="text-4xl font-bold mb-8">Latest Posts</h1>
    {% if posts %}
        {% for post in posts %}
        <div class="bg-white p-6 rounded shadow mb-6">
            <h2 class="text-2xl font-semibold">{{ post.title }}</h2>
            <small class="text-gray-500">Posted on {{ post.date }}</small>
            <p class="mt-4">{{ post.content[:200] }}...</p>
            <a href="/post/{{ loop.index0 }}" class="text-blue-600 hover:underline">Read More →</a>
        </div>
        {% endfor %}
    {% else %}
        <p class="text-center text-gray-500 py-10">No posts yet. Login as admin to create one!</p>
    {% endif %}
    ''')
    return render_template_string(html, posts=posts)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    if post_id >= len(posts):
        return "Post not found", 404
    post = posts[post_id]
    html = BASE_HTML.replace('{% block content %}{% endblock %}', f'''
    <a href="/" class="text-blue-600 mb-4 inline-block">← Back to Home</a>
    <h1 class="text-3xl font-bold mb-2">{post["title"]}</h1>
    <small class="text-gray-500">Posted on {post["date"]}</small>
    <div class="mt-8 prose">
        <p style="white-space: pre-wrap;">{post["content"]}</p>
    </div>
    ''')
    return render_template_string(html)

# ====================== ADMIN ======================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect('/dashboard')
        return "Wrong username or password! <a href='/login'>Try again</a>"
    
    html = BASE_HTML.replace('{% block content %}{% endblock %}', '''
    <div class="max-w-md mx-auto bg-white p-8 rounded shadow">
        <h2 class="text-2xl font-bold mb-6 text-center">Admin Login</h2>
        <form method="post">
            <input type="text" name="username" placeholder="Username" class="w-full p-3 border mb-4 rounded" required><br>
            <input type="password" name="password" placeholder="Password" class="w-full p-3 border mb-6 rounded" required><br>
            <button type="submit" class="w-full bg-blue-600 text-white py-3 rounded font-semibold">Login</button>
        </form>
        <p class="text-center text-sm mt-4 text-gray-500">Default: admin / admin123</p>
    </div>
    ''')
    return render_template_string(html)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            posts.insert(0, {
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%B %d, %Y")
            })
            return redirect('/')
    
    html = BASE_HTML.replace('{% block content %}{% endblock %}', '''
    <h2 class="text-3xl font-bold mb-6">Admin Dashboard</h2>
    <form method="post" class="bg-white p-6 rounded shadow">
        <input type="text" name="title" placeholder="Post Title" class="w-full p-3 border mb-4 rounded" required>
        <textarea name="content" rows="10" placeholder="Write your blog post here..." class="w-full p-3 border mb-4 rounded" required></textarea>
        <button type="submit" class="bg-green-600 text-white px-6 py-3 rounded font-semibold">Publish Post</button>
    </form>
    ''')
    return render_template_string(html)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ====================== RUN ======================
if __name__ == '__main__':
    print("🚀 Blog Website is starting...")
    print("Go to: http://127.0.0.1:5000")
    print("Login with → Username: admin | Password: admin123")
    app.run(debug=True)