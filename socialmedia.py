from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

posts = []

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Social Media Website</title>
<style>
body{
    font-family:Arial;
    background:#f0f2f5;
    margin:0;
}
.header{
    background:#1877f2;
    color:white;
    padding:15px;
    text-align:center;
}
.container{
    width:60%;
    margin:auto;
    margin-top:20px;
}
.post-box{
    background:white;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;
}
textarea{
    width:100%;
    height:80px;
}
button{
    background:#1877f2;
    color:white;
    border:none;
    padding:10px 20px;
    cursor:pointer;
}
.post{
    background:white;
    padding:15px;
    border-radius:10px;
    margin-top:10px;
}
</style>
</head>
<body>

<div class="header">
<h1>📱 My Social Media</h1>
</div>

<div class="container">

<div class="post-box">
<form method="POST" action="/post">
<textarea name="content" placeholder="What's on your mind?" required></textarea>
<br><br>
<button type="submit">Post</button>
</form>
</div>

{% for post in posts %}
<div class="post">
<h3>User</h3>
<p>{{ post }}</p>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, posts=reversed(posts))

@app.route("/post", methods=["POST"])
def add_post():
    content = request.form["content"]
    posts.append(content)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)