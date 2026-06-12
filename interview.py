from flask import Flask, request, render_template_string

app = Flask(__name__)

questions = [
    "What is Python?",
    "What is Flask?",
    "What is a Database?",
    "Explain OOP concepts.",
    "What is HTML?"
]

html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Interview System</title>
<style>
body{
    font-family:Arial;
    background:linear-gradient(135deg,#4e54c8,#8f94fb);
    padding:30px;
}
.container{
    max-width:800px;
    margin:auto;
    background:white;
    padding:25px;
    border-radius:15px;
    box-shadow:0 0 15px gray;
}
h1{text-align:center;}
textarea{
    width:100%;
    height:60px;
    margin-bottom:15px;
}
button{
    background:#28a745;
    color:white;
    padding:12px 20px;
    border:none;
    cursor:pointer;
}
.result{
    background:#f4f4f4;
    padding:15px;
    margin-top:20px;
    border-radius:10px;
}
</style>
</head>
<body>

<div class="container">
<h1>🎤 AI Interview System</h1>

<form method="POST">

{% for q in questions %}
<p><b>{{ loop.index }}. {{ q }}</b></p>
<textarea name="answer{{ loop.index }}" required></textarea>
{% endfor %}

<button type="submit">Submit Interview</button>

</form>

{% if result %}
<div class="result">
<h2>Interview Result</h2>

<p><b>Score:</b> {{ result.score }}/100</p>
<p><b>Performance:</b> {{ result.performance }}</p>

<h3>Feedback</h3>
<ul>
{% for item in result.feedback %}
<li>{{ item }}</li>
{% endfor %}
</ul>

</div>
{% endif %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    result = None

    if request.method == "POST":

        score = 0

        feedback = []

        keywords = [
            ["programming", "language", "python"],
            ["framework", "flask", "web"],
            ["database", "data", "storage"],
            ["class", "object", "inheritance"],
            ["html", "web", "markup"]
        ]

        for i in range(5):

            answer = request.form.get(f"answer{i+1}", "").lower()

            matches = 0

            for word in keywords[i]:
                if word in answer:
                    matches += 1

            if matches >= 2:
                score += 20
                feedback.append(
                    f"Question {i+1}: Good Answer"
                )
            else:
                feedback.append(
                    f"Question {i+1}: Needs Improvement"
                )

        if score >= 80:
            performance = "Excellent"
        elif score >= 60:
            performance = "Good"
        elif score >= 40:
            performance = "Average"
        else:
            performance = "Poor"

        result = {
            "score": score,
            "performance": performance,
            "feedback": feedback
        }

    return render_template_string(
        html,
        questions=questions,
        result=result
    )

if __name__ == "__main__":
    app.run(debug=True)