from flask import Flask, render_template_string

app = Flask(__name__)

clicks = 1250
sales = 87
commission = 15430

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Affiliate Marketing Dashboard</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    margin:0;
}
.header{
    background:#2563eb;
    color:white;
    text-align:center;
    padding:20px;
}
.container{
    width:90%;
    margin:auto;
    padding:20px;
}
.cards{
    display:flex;
    gap:20px;
    flex-wrap:wrap;
}
.card{
    background:white;
    padding:20px;
    flex:1;
    min-width:200px;
    border-radius:10px;
    box-shadow:0 0 10px #ccc;
    text-align:center;
}
.link-box{
    background:white;
    padding:20px;
    margin-top:20px;
    border-radius:10px;
}
input{
    width:100%;
    padding:10px;
}
</style>
</head>
<body>

<div class="header">
    <h1>💰 Affiliate Marketing Dashboard</h1>
</div>

<div class="container">

<div class="cards">

<div class="card">
    <h2>Total Clicks</h2>
    <h1>{{ clicks }}</h1>
</div>

<div class="card">
    <h2>Total Sales</h2>
    <h1>{{ sales }}</h1>
</div>

<div class="card">
    <h2>Commission Earned</h2>
    <h1>₹{{ commission }}</h1>
</div>

</div>

<div class="link-box">
    <h2>Your Affiliate Link</h2>
    <input type="text"
    value="https://example.com/?ref=affiliate123"
    readonly>
</div>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        clicks=clicks,
        sales=sales,
        commission=commission
    )

if __name__ == "__main__":
    app.run(debug=True)