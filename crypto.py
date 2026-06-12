from flask import Flask, render_template_string

app = Flask(__name__)

cryptos = [
    {"name": "Bitcoin", "symbol": "BTC", "price": "$105,000", "change": "+2.5%"},
    {"name": "Ethereum", "symbol": "ETH", "price": "$5,200", "change": "+1.8%"},
    {"name": "Solana", "symbol": "SOL", "price": "$220", "change": "-0.9%"},
    {"name": "Cardano", "symbol": "ADA", "price": "$0.95", "change": "+3.2%"}
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Crypto Tracker</title>
<style>
body{
    font-family:Arial;
    background:#0f172a;
    color:white;
    margin:0;
}
.header{
    text-align:center;
    padding:20px;
    background:#1e293b;
}
.container{
    width:90%;
    margin:auto;
    padding:20px;
}
.card{
    background:#1e293b;
    padding:20px;
    margin:10px 0;
    border-radius:10px;
}
.price{
    font-size:24px;
    font-weight:bold;
}
</style>
</head>
<body>

<div class="header">
    <h1>₿ Crypto Tracking App</h1>
</div>

<div class="container">
{% for coin in cryptos %}
<div class="card">
    <h2>{{ coin.name }} ({{ coin.symbol }})</h2>
    <div class="price">{{ coin.price }}</div>
    <p>24H Change: {{ coin.change }}</p>
</div>
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, cryptos=cryptos)

if __name__ == "__main__":
    app.run(debug=True)