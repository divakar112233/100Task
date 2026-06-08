from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "ecommerce-secret-key"

# Sample Products
products = {
    1: {"id": 1, "name": "Wireless Headphones", "price": 1299, "description": "Premium noise-cancelling headphones.", "image": "https://picsum.photos/id/20/600/400", "category": "Electronics"},
    2: {"id": 2, "name": "Smart Watch", "price": 2499, "description": "Fitness smartwatch with heart rate monitor.", "image": "https://picsum.photos/id/201/600/400", "category": "Wearables"},
    3: {"id": 3, "name": "Laptop Backpack", "price": 899, "description": "Water-resistant laptop backpack.", "image": "https://picsum.photos/id/180/600/400", "category": "Fashion"}
}

@app.route('/')
def home():
    return render_template_string("""
    <div class="max-w-6xl mx-auto p-6">
        <h1 class="text-4xl font-bold text-center mb-10">🛒 My Store</h1>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            {% for product in products.values() %}
            <div class="bg-white rounded-2xl shadow hover:shadow-xl transition overflow-hidden">
                <img src="{{ product.image }}" class="w-full h-56 object-cover">
                <div class="p-6">
                    <h3 class="font-bold text-xl">{{ product.name }}</h3>
                    <p class="text-gray-500">{{ product.category }}</p>
                    <p class="text-2xl font-semibold mt-2">₹{{ product.price }}</p>
                    <a href="/product/{{ product.id }}" class="block text-center mt-4 bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700">
                        View Details
                    </a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    """, products=products)

@app.route('/product/<int:product_id>')
def product_page(product_id):
    product = products.get(product_id)
    if not product:
        return "Product not found", 404

    cart_count = len(session.get('cart', []))

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{{ product.name }}</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-50">
        <div class="max-w-5xl mx-auto p-6">
            <a href="/" class="text-blue-600 hover:underline mb-6 inline-block">← Back to Shop</a>
            
            <div class="grid md:grid-cols-2 gap-10 bg-white rounded-3xl shadow-xl p-8">
                <div>
                    <img src="{{ product.image }}" class="w-full rounded-2xl shadow">
                </div>
                <div>
                    <h1 class="text-4xl font-bold mb-2">{{ product.name }}</h1>
                    <p class="text-gray-500 mb-4">{{ product.category }}</p>
                    <div class="text-4xl font-bold text-green-600 mb-6">₹{{ product.price }}</div>
                    <p class="text-gray-700 leading-relaxed text-lg mb-8">{{ product.description }}</p>
                    
                    <div class="flex gap-4">
                        <form method="post" action="/add-to-cart/{{ product.id }}">
                            <button type="submit" class="bg-blue-600 hover:bg-blue-700 text-white px-10 py-4 rounded-2xl font-semibold text-lg">
                                🛒 Add to Cart
                            </button>
                        </form>
                        <a href="/cart" class="border border-gray-300 hover:bg-gray-100 px-8 py-4 rounded-2xl font-semibold">
                            Cart ({{ cart_count }})
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, product=product, cart_count=cart_count)

@app.route('/add-to-cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    if product_id not in session['cart']:
        session['cart'].append(product_id)
    return redirect(url_for('product_page', product_id=product_id))

@app.route('/cart')
def cart():
    cart_items = [products[pid] for pid in session.get('cart', [])]
    total = sum(item['price'] for item in cart_items)

    html = """
    <div class="max-w-4xl mx-auto p-6">
        <h1 class="text-3xl font-bold mb-8">Your Cart</h1>
        {% if cart_items %}
            <div class="space-y-6">
                {% for item in cart_items %}
                <div class="flex justify-between items-center bg-white p-6 rounded-2xl shadow">
                    <div class="flex gap-6">
                        <img src="{{ item.image }}" class="w-24 h-24 object-cover rounded-xl">
                        <div>
                            <h3 class="font-semibold">{{ item.name }}</h3>
                            <p class="text-gray-500">₹{{ item.price }}</p>
                        </div>
                    </div>
                    <p class="text-2xl font-bold">₹{{ item.price }}</p>
                </div>
                {% endfor %}
            </div>
            
            <div class="mt-10 bg-white p-8 rounded-3xl shadow text-right">
                <p class="text-2xl">Total: <span class="font-bold">₹{{ total }}</span></p>
                <button onclick="alert('Thank you for shopping! (Demo)')" 
                        class="mt-6 bg-green-600 text-white px-12 py-4 rounded-2xl text-lg font-semibold">
                    Proceed to Checkout
                </button>
            </div>
        {% else %}
            <p class="text-center text-2xl text-gray-500 py-20">Your cart is empty</p>
        {% endif %}
        <a href="/" class="block text-center mt-8 text-blue-600">← Continue Shopping</a>
    </div>
    """
    return render_template_string(html, cart_items=cart_items, total=total)

if __name__ == '__main__':
    print("🚀 E-Commerce Store Running at http://127.0.0.1:5000")
    app.run(debug=True)