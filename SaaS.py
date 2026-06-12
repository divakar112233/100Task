from flask import Flask, render_template_string, request

app = Flask(__name__)

plans = [
    {"name": "Basic", "price": "₹199/month"},
    {"name": "Pro", "price": "₹499/month"},
    {"name": "Enterprise", "price": "₹999/month"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>SaaS Subscription Platform</title>
    <style>
        body{
            font-family:Arial;
            background:#f4f4f4;
            text-align:center;
            margin:0;
        }
        .header{
            background:#4f46e5;
            color:white;
            padding:20px;
        }
        .plans{
            display:flex;
            justify-content:center;
            gap:20px;
            margin-top:40px;
            flex-wrap:wrap;
        }
        .card{
            background:white;
            padding:20px;
            width:250px;
            border-radius:10px;
            box-shadow:0 0 10px #ccc;
        }
        button{
            background:#4f46e5;
            color:white;
            border:none;
            padding:10px 20px;
            cursor:pointer;
            border-radius:5px;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>🚀 My SaaS Platform</h1>
    <p>Choose a subscription plan</p>
</div>

<div class="plans">
{% for plan in plans %}
<div class="card">
    <h2>{{ plan.name }}</h2>
    <h3>{{ plan.price }}</h3>
    <form method="post">
        <input type="hidden" name="plan" value="{{ plan.name }}">
        <button type="submit">Subscribe</button>
    </form>
</div>
{% endfor %}
</div>

{% if message %}
<h2>{{ message }}</h2>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    if request.method == "POST":
        plan = request.form["plan"]
        message = f"You subscribed to the {plan} plan!"
    return render_template_string(HTML, plans=plans, message=message)

if __name__ == "__main__":
    app.run(debug=True)