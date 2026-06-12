from flask import Flask, request, render_template_string
import requests
import time

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Website Performance Checker</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    padding:20px;
}
.container{
    max-width:700px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:10px;
    box-shadow:0 0 10px #ccc;
}
input{
    width:100%;
    padding:10px;
}
button{
    margin-top:10px;
    padding:10px 20px;
    background:#2563eb;
    color:white;
    border:none;
    cursor:pointer;
}
.result{
    margin-top:20px;
    padding:15px;
    background:#eef;
    border-radius:10px;
}
</style>
</head>
<body>

<div class="container">
<h1>⚡ Website Performance Checker</h1>

<form method="POST">
<input type="text" name="url" placeholder="https://example.com" required>
<button type="submit">Check Performance</button>
</form>

{% if result %}
<div class="result">
{{ result|safe }}
</div>
{% endif %}

</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        url = request.form["url"]

        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            end = time.time()

            load_time = round(end - start, 2)
            size = round(len(response.content) / 1024, 2)

            result = f"""
            <h3>Performance Report</h3>
            <p><b>Status Code:</b> {response.status_code}</p>
            <p><b>Load Time:</b> {load_time} seconds</p>
            <p><b>Page Size:</b> {size} KB</p>
            <p><b>Server:</b> {response.headers.get('Server','Unknown')}</p>
            """

        except Exception as e:
            result = f"<p>Error: {e}</p>"

    return render_template_string(HTML, result=result)

if __name__ == "__main__":
    app.run(debug=True)