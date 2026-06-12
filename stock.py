from flask import Flask, render_template_string

app = Flask(__name__)

stocks = [
    {"symbol": "AAPL", "price": 210.45, "change": "+1.25%"},
    {"symbol": "GOOGL", "price": 182.30, "change": "-0.80%"},
    {"symbol": "TSLA", "price": 325.75, "change": "+2.10%"},
    {"symbol": "MSFT", "price": 512.40, "change": "+0.95%"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock Market Dashboard</title>
    <style>
        body{
            font-family:Arial;
            background:#f4f4f4;
            margin:0;
        }
        .header{
            background:#111827;
            color:white;
            text-align:center;
            padding:20px;
        }
        .container{
            width:90%;
            margin:auto;
            padding:20px;
        }
        .card{
            background:white;
            padding:20px;
            margin:10px 0;
            border-radius:10px;
            box-shadow:0 0 10px #ddd;
        }
        .price{
            font-size:24px;
            font-weight:bold;
        }
        .change{
            color:green;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>📈 Stock Market Dashboard</h1>
</div>

<div class="container">
    {% for stock in stocks %}
    <div class="card">
        <h2>{{ stock.symbol }}</h2>
        <div class="price">${{ stock.price }}</div>
        <div class="change">{{ stock.change }}</div>
    </div>
    {% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, stocks=stocks)

if __name__ == "__main__":
    app.run(debug=True)