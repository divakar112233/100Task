from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "shopping-cart-secret"

# Sample Products
products = {
    1: {"id": 1, "name": "Wireless Headphones", "price": 1299, "image": "https://picsum.photos/id/20/300/200"},
    2: {"id": 2, "name": "Smart Watch", "price": 2499, "image": "https://picsum.photos/id/201/300/200"},
    3: {"id": 3, "name": "Laptop Backpack", "price": 899, "image": "https://picsum.photos/id/180/300/200"},
    4: {"id": 4, "name": "Bluetooth Speaker", "price": 799, "image": "https://picsum.photos/id/60/300/200"},
}

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shop</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-gray-100">
        <div class="max-w-6xl mx-auto p-6">
            <div class="flex justify-between items-center mb-8">
                <h1 class="text-4xl font-bold">🛍️ My Shop</h1>
                <a href="/cart" class="bg-blue-600 text-white px-6 py-3 rounded-xl font-semibold flex items-center gap-2">
                    🛒 Cart ({{ cart_count }})
                </a>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                {% for product in products.values() %}
                <div class="bg-white rounded-2xl shadow hover:shadow-2xl transition p-4">
                    <img src="{{ product.image }}" class="w-full h-48 object-cover rounded-xl">
                    <h3 class="font-semibold mt-4">{{ product.name }}</h3>
                    <p class="text-2xl font-bold text-green-600 mt-1">₹{{ product.price }}</p>
                    <a href="/product/{{ product.id }}" 
                       class="block mt-4 text-center bg-blue-600 text-white py-3 rounded-xl hover:bg-blue-700">
                        View Product
                    </a>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """, products=products, cart_count=len(session.get('cart', [])))

@app.route('/product/<int:pid>')
def product(pid):
    product = products.get(pid)
    if not product:
        return "Product not found"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>{{ product.name }}</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-gray-100 p-6">
        <div class="max-w-4xl mx-auto bg-white rounded-3xl shadow p-8">
            <a href="/" class="text-blue-600 mb-6 inline-block">← Back to Shop</a>
            <div class="grid md:grid-cols-2 gap-10">
                <img src="{{ product.image }}" class="rounded-2xl">
                <div>
                    <h1 class="text-4xl font-bold">{{ product.name }}</h1>
                    <p class="text-4xl font-bold text-green-600 mt-4">₹{{ product.price }}</p>
                    <p class="mt-6 text-gray-600">High quality product with excellent performance.</p>
                    
                    <form method="post" action="/add-to-cart/{{ product.id }}">
                        <button type="submit" 
                                class="mt-8 w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-2xl text-xl font-semibold">
                            🛒 Add to Cart
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, product=product)

@app.route('/add-to-cart/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    if 'cart' not in session:
        session['cart'] = []
    if pid not in session['cart']:
        session['cart'].append(pid)
    return redirect(url_for('product', pid=pid))

@app.route('/cart')
def view_cart():
    cart_ids = session.get('cart', [])
    cart_items = [products[i] for i in cart_ids if i in products]
    total = sum(item['price'] for item in cart_items)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Cart</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-gray-100 p-6">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl font-bold mb-8">Your Shopping Cart</h1>
            
            {% if cart_items %}
                <div class="space-y-6">
                    {% for item in cart_items %}
                    <div class="flex items-center justify-between bg-white p-6 rounded-2xl shadow">
                        <div class="flex items-center gap-6">
                            <img src="{{ item.image }}" class="w-24 h-24 object-cover rounded-xl">
                            <div>
                                <h3 class="font-semibold text-xl">{{ item.name }}</h3>
                                <p class="text-2xl font-bold">₹{{ item.price }}</p>
                            </div>
                        </div>
                        <form method="post" action="/remove/{{ item.id }}">
                            <button type="submit" class="text-red-600 hover:text-red-700 font-medium">Remove</button>
                        </form>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="mt-10 bg-white p-8 rounded-3xl shadow">
                    <div class="flex justify-between text-3xl font-bold">
                        <span>Total:</span>
                        <span>₹{{ total }}</span>
                    </div>
                    <button onclick="alert('🎉 Order placed successfully! (Demo)')" 
                            class="mt-8 w-full bg-green-600 text-white py-5 rounded-2xl text-xl font-semibold">
                        Proceed to Checkout
                    </button>
                </div>
            {% else %}
                <p class="text-center text-2xl text-gray-500 py-20">Your cart is empty</p>
            {% endif %}
            
            <div class="text-center mt-8">
                <a href="/" class="text-blue-600 text-lg">← Continue Shopping</a>
            </div>
        </div>
    </body>
    </html>
    """, cart_items=cart_items, total=total)

@app.route('/remove/<int:pid>', methods=['POST'])
def remove_from_cart(pid):
    if 'cart' in session and pid in session['cart']:
        session['cart'].remove(pid)
    return redirect('/cart')

@app.route('/clear-cart')
def clear_cart():
    session.pop('cart', None)
    return redirect('/cart')

if __name__ == '__main__':
    print("🚀 Shopping Cart System Running...")
    print("Open → http://127.0.0.1:5000")
    app.run(debug=True)