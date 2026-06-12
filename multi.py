from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

products = [
    {
        "vendor": "Tech Store",
        "name": "Laptop",
        "price": 50000
    },
    {
        "vendor": "Mobile Hub",
        "name": "Smartphone",
        "price": 20000
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Multi Vendor Store</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    margin:0;
}
.header{
    background:#28a745;
    color:white;
    text-align:center;
    padding:15px;
}
.container{
    width:80%;
    margin:auto;
    padding:20px;
}
.card{
    background:white;
    padding:15px;
    margin:10px 0;
    border-radius:10px;
    box-shadow:0 0 5px #ccc;
}
input{
    width:100%;
    padding:10px;
    margin:5px 0;
}
button{
    background:#28a745;
    color:white;
    border:none;
    padding:10px;
    cursor:pointer;
}
</style>
</head>
<body>

<div class="header">
<h1>🛒 Multi Vendor E-Commerce Platform</h1>
</div>

<div class="container">

<h2>Add Product</h2>

<form method="POST" action="/add">
<input type="text" name="vendor" placeholder="Vendor Name" required>
<input type="text" name="name" placeholder="Product Name" required>
<input type="number" name="price" placeholder="Price" required>
<button type="submit">Add Product</button>
</form>

<hr>

<h2>Products</h2>

{% for p in products %}
<div class="card">
<h3>{{ p.name }}</h3>
<p>Vendor: {{ p.vendor }}</p>
<p>Price: ₹{{ p.price }}</p>
<button onclick="alert('Added to Cart')">
Add to Cart
</button>
</div>
{% endfor %}

</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, products=products)

@app.route("/add", methods=["POST"])
def add():
    products.append({
        "vendor": request.form["vendor"],
        "name": request.form["name"],
        "price": request.form["price"]
    })
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)