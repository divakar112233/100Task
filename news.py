from flask import Flask, render_template_string

app = Flask(__name__)

news = [
    {
        "title": "Technology News",
        "content": "Artificial Intelligence is transforming industries worldwide.",
        "image": "https://picsum.photos/800/400?random=1"
    },
    {
        "title": "Sports Update",
        "content": "Major tournaments are attracting millions of fans.",
        "image": "https://picsum.photos/800/400?random=2"
    },
    {
        "title": "World News",
        "content": "Global leaders discuss economic growth and innovation.",
        "image": "https://picsum.photos/800/400?random=3"
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Daily News Portal</title>
    <style>
        body{
            margin:0;
            font-family:Arial,sans-serif;
            background:#f4f6f9;
        }

        .header{
            background:#0d6efd;
            color:white;
            text-align:center;
            padding:25px;
        }

        .container{
            width:90%;
            max-width:1100px;
            margin:20px auto;
        }

        .card{
            background:white;
            border-radius:10px;
            overflow:hidden;
            margin-bottom:25px;
            box-shadow:0 4px 10px rgba(0,0,0,0.15);
        }

        .card img{
            width:100%;
            height:300px;
            object-fit:cover;
        }

        .content{
            padding:20px;
        }

        h2{
            color:#333;
        }

        .footer{
            background:#222;
            color:white;
            text-align:center;
            padding:15px;
            margin-top:20px;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>📰 Daily News Portal</h1>
    <p>Latest News Around The World</p>
</div>

<div class="container">
{% for item in news %}
<div class="card">
    <img src="{{ item.image }}">
    <div class="content">
        <h2>{{ item.title }}</h2>
        <p>{{ item.content }}</p>
    </div>
</div>
{% endfor %}
</div>

<div class="footer">
    © 2026 Daily News Portal
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, news=news)

if __name__ == "__main__":
    app.run(debug=True)