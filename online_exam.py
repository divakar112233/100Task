from flask import Flask, render_template_string, request

app = Flask(__name__)

questions = [
    {
        "question": "What is the capital of India?",
        "options": ["Delhi", "Mumbai", "Chennai", "Kolkata"],
        "answer": "Delhi"
    },
    {
        "question": "Which language is used for Python web development?",
        "options": ["HTML", "Flask", "Java", "C++"],
        "answer": "Flask"
    },
    {
        "question": "2 + 2 = ?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Examination System</title>
    <style>
        body{
            font-family: Arial;
            background:#f4f4f4;
            margin:0;
        }
        .container{
            width:70%;
            margin:30px auto;
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px gray;
        }
        h1{
            text-align:center;
            color:#007bff;
        }
        button{
            background:#007bff;
            color:white;
            border:none;
            padding:10px 20px;
            cursor:pointer;
            border-radius:5px;
        }
    </style>
</head>
<body>

<div class="container">
<h1>📝 Online Examination System</h1>

<form method="POST">

{% for q in questions %}
<p><b>{{ loop.index }}. {{ q.question }}</b></p>

{% for option in q.options %}
<input type="radio" name="q{{ loop.parent.index0 }}" value="{{ option }}" required>
{{ option }}<br>
{% endfor %}

<hr>
{% endfor %}

<button type="submit">Submit Exam</button>

</form>

{% if score is not none %}
<h2>Your Score: {{ score }}/{{ total }}</h2>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def exam():
    score = None

    if request.method == "POST":
        score = 0

        for i, q in enumerate(questions):
            user_answer = request.form.get(f"q{i}")
            if user_answer == q["answer"]:
                score += 1

    return render_template_string(
        HTML,
        questions=questions,
        score=score,
        total=len(questions)
    )

if __name__ == "__main__":
    app.run(debug=True)