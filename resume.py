from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
<title>AI Resume Analyzer</title>
<style>
body{
    font-family:Arial;
    background:linear-gradient(135deg,#2193b0,#6dd5ed);
    margin:0;
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
h1{
    text-align:center;
}
textarea{
    width:100%;
    height:250px;
    padding:10px;
}
button{
    background:#28a745;
    color:white;
    border:none;
    padding:12px 25px;
    margin-top:10px;
    cursor:pointer;
}
.result{
    margin-top:20px;
    background:#f5f5f5;
    padding:15px;
    border-radius:10px;
}
</style>
</head>
<body>

<div class="container">
<h1>📄 AI Resume Analyzer</h1>

<form method="POST">
<textarea name="resume"
placeholder="Paste your resume here..." required></textarea>
<br>
<button type="submit">Analyze Resume</button>
</form>

{% if result %}
<div class="result">
<h2>Analysis Report</h2>

<p><b>Resume Score:</b> {{ result.score }}/100</p>

<p><b>Detected Skills:</b></p>
<ul>
{% for skill in result.skills %}
<li>{{ skill }}</li>
{% endfor %}
</ul>

<p><b>Suggestions:</b></p>
<ul>
{% for tip in result.tips %}
<li>{{ tip }}</li>
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

        resume = request.form["resume"].lower()

        skills_db = [
            "python","java","html","css",
            "javascript","sql","django",
            "flask","react","mongodb"
        ]

        found_skills = []

        for skill in skills_db:
            if skill in resume:
                found_skills.append(skill)

        score = min(len(found_skills) * 10, 100)

        tips = []

        if len(found_skills) < 3:
            tips.append("Add more technical skills.")

        if "project" not in resume:
            tips.append("Include project experience.")

        if "internship" not in resume:
            tips.append("Add internship experience.")

        if "education" not in resume:
            tips.append("Mention educational qualifications.")

        if score >= 70:
            tips.append("Strong resume profile.")
        else:
            tips.append("Resume needs improvement.")

        result = {
            "score": score,
            "skills": found_skills,
            "tips": tips
        }

    return render_template_string(html, result=result)

if __name__ == "__main__":
    app.run(debug=True)