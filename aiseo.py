from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI SEO Analyzer</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    padding:20px;
}
.container{
    max-width:800px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:10px;
}
input{
    width:100%;
    padding:10px;
}
button{
    padding:10px 20px;
    background:#2563eb;
    color:white;
    border:none;
    margin-top:10px;
}
.result{
    margin-top:20px;
    background:#eef;
    padding:15px;
}
</style>
</head>
<body>

<div class="container">
<h1>🔍 AI SEO Analyzer Tool</h1>

<form method="POST">
<input type="text" name="url" placeholder="Enter Website URL" required>
<button type="submit">Analyze</button>
</form>

{% if report %}
<div class="result">
{{ report|safe }}
</div>
{% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    report = ""

    if request.method == "POST":
        url = request.form["url"]

        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.text, "html.parser")

            title = soup.title.string if soup.title else "Missing"
            meta = soup.find("meta", attrs={"name":"description"})
            meta_desc = meta["content"] if meta else "Missing"

            score = 100

            if title == "Missing":
                score -= 30

            if meta_desc == "Missing":
                score -= 30

            report = f"""
            <h2>SEO Report</h2>
            <p><b>Title:</b> {title}</p>
            <p><b>Meta Description:</b> {meta_desc}</p>
            <p><b>SEO Score:</b> {score}/100</p>
            """

        except Exception as e:
            report = f"<h3>Error: {e}</h3>"

    return render_template_string(HTML, report=report)

if __name__ == "__main__":
    app.run(debug=True)