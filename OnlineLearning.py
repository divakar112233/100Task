from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

courses = [
    {"title": "Python Basics", "description": "Learn Python from scratch."},
    {"title": "Web Development", "description": "Learn HTML, CSS and Flask."},
    {"title": "Database Fundamentals", "description": "Learn SQL and databases."}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Online LMS</title>
    <style>
        body{
            font-family:Arial;
            background:#f4f4f4;
            margin:0;
        }
        .header{
            background:#007bff;
            color:white;
            padding:15px;
            text-align:center;
        }
        .container{
            width:80%;
            margin:auto;
            padding:20px;
        }
        .course{
            background:white;
            padding:15px;
            margin:10px 0;
            border-radius:10px;
            box-shadow:0 0 5px gray;
        }
        button{
            background:#007bff;
            color:white;
            border:none;
            padding:10px;
            border-radius:5px;
            cursor:pointer;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>🎓 Online Learning Management System</h1>
</div>

<div class="container">
    <h2>Available Courses</h2>

    {% for course in courses %}
    <div class="course">
        <h3>{{ course.title }}</h3>
        <p>{{ course.description }}</p>
        <button onclick="alert('Enrolled Successfully!')">
            Enroll Now
        </button>
    </div>
    {% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, courses=courses)

if __name__ == "__main__":
    app.run(debug=True)