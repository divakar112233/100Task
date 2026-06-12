from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Security Header Scanner</title>
    <style>
        body{font-family:Arial;background:#f4f4f4;padding:20px;}
        .box{background:white;padding:20px;border-radius:10px;max-width:800px;margin:auto;}
        input{width:100%;padding:10px;}
        button{padding:10px 20px;margin-top:10px;}
        table{width:100%;border-collapse:collapse;margin-top:20px;}
        td,th{border:1px solid #ddd;padding:8px;}
    </style>
</head>
<body>
<div class="box">
    <h1>🛡️ Website Security Scanner</h1>

    <form method="POST">
        <input type="text" name="url" placeholder="https://example.com" required>
        <button type="submit">Scan</button>
    </form>

    {% if results %}
    <table>
        <tr>
            <th>Security Header</th>
            <th>Status</th>
        </tr>
        {% for item in results %}
        <tr>
            <td>{{ item[0] }}</td>
            <td>{{ item[1] }}</td>
        </tr>
        {% endfor %}
    </table>
    {% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        url = request.form["url"]

        try:
            r = requests.get(url, timeout=10)

            headers_to_check = [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "Referrer-Policy"
            ]

            for header in headers_to_check:
                if header in r.headers:
                    results.append((header, "✅ Present"))
                else:
                    results.append((header, "❌ Missing"))

        except Exception as e:
            results.append(("Error", str(e)))

    return render_template_string(HTML, results=results)

if __name__ == "__main__":
    app.run(debug=True)