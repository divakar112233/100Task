from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Project Management SaaS</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    margin:0;
}
.header{
    background:#2563eb;
    color:white;
    text-align:center;
    padding:15px;
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
input, textarea{
    width:100%;
    padding:10px;
    margin:5px 0;
}
button{
    background:#2563eb;
    color:white;
    border:none;
    padding:10px 20px;
    cursor:pointer;
}
</style>
</head>
<body>

<div class="header">
<h1>📋 Project Management SaaS</h1>
</div>

<div class="container">

<h2>Create Task</h2>

<form method="POST" action="/add">
<input type="text" name="title" placeholder="Task Title" required>

<textarea name="description"
placeholder="Task Description"></textarea>

<button type="submit">Add Task</button>
</form>

<hr>

<h2>Project Tasks</h2>

{% for task in tasks %}
<div class="card">
<h3>{{ task.title }}</h3>
<p>{{ task.description }}</p>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    tasks.append({
        "title": request.form["title"],
        "description": request.form["description"]
    })
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)