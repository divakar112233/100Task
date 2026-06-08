from flask import Flask, render_template_string, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "foodapp-secret-key"

# Menu Items
menu = {
    1: {"id": 1, "name": "Margherita Pizza", "price": 249, "category": "Pizza", "image": "https://picsum.photos/id/1080/300/200"},
    2: {"id": 2, "name": "Butter Chicken", "price": 320, "category": "Indian", "image": "https://picsum.photos/id/292/300/200"},
    3: {"id": 3, "name": "Veg Burger", "price": 149, "category": "Fast Food", "image": "https://picsum.photos/id/431/300/200"},
    4: {"id": 4, "name": "Paneer Fried Rice", "price": 180, "category": "Rice", "image": "https://picsum.photos/id/870/300/200"},
    5: {"id": 5, "name": "Chocolate Shake", "price": 120, "category": "Drinks", "image": "https://picsum.photos/id/201/300/200"},
    6: {"id": 6, "name": "French Fries", "price": 99, "category": "Snacks", "image": "https://picsum.photos/id/292/300/200"},
}

@app.route('/')
def home():
    cart_count = len(session.get('cart', []))
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>FoodOrder</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-orange-50">
        <div class="max-w-6xl mx-auto p-6">
            <div class="flex justify-between items-center mb-8">
                <h1 class="text-4xl font-bold text-orange-600">🍔 FoodOrder</h1>
                <a href="/cart" class="bg-orange-600 text-white px-6 py-3 rounded-2xl font-semibold flex items-center gap-2">
                    🛒 Cart ({{ cart_count }})
                </a>
            </div>
            
            <h2 class="text-2xl font-semibold mb-6">Our Menu</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {% for item in menu.values() %}
                <div class="bg-white rounded-3xl shadow hover:shadow-xl transition overflow-hidden">
                    <img src="{{ item.image }}" class="w-full h-48 object-cover">
                    <div class="p-5">
                        <h3 class="font-bold text-xl">{{ item.name }}</h3>
                        <p class="text-orange-500">{{ item.category }}</p>
                        <p class="text-2xl font-bold mt-2">₹{{ item.price }}</p>
                        <a href="/item/{{ item.id }}" 
                           class="block mt-4 text-center bg-orange-600 text-white py-3 rounded-2xl hover:bg-orange-700">
                            View & Add
                        </a>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """, menu=menu, cart_count=cart_count)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = menu.get(item_id)
    if not item:
        return "Item not found"
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>{{ item.name }}</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-orange-50 p-6">
        <div class="max-w-4xl mx-auto bg-white rounded-3xl shadow p-8">
            <a href="/" class="text-orange-600 mb-6 inline-block">← Back to Menu</a>
            <div class="grid md:grid-cols-2 gap-10">
                <img src="{{ item.image }}" class="rounded-3xl">
                <div>
                    <h1 class="text-4xl font-bold">{{ item.name }}</h1>
                    <p class="text-orange-500 text-xl">{{ item.category }}</p>
                    <p class="text-4xl font-bold text-green-600 mt-6">₹{{ item.price }}</p>
                    <p class="mt-6 text-gray-600">Delicious and fresh prepared food. Best in town!</p>
                    
                    <form method="post" action="/add-to-cart/{{ item.id }}">
                        <button type="submit" 
                                class="mt-10 w-full bg-orange-600 hover:bg-orange-700 text-white py-5 rounded-3xl text-xl font-semibold">
                            🛒 Add to Cart
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    """, item=item)

@app.route('/add-to-cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    if 'cart' not in session:
        session['cart'] = []
    if item_id not in session['cart']:
        session['cart'].append(item_id)
    return redirect(url_for('item_detail', item_id=item_id))

@app.route('/cart')
def view_cart():
    cart_ids = session.get('cart', [])
    cart_items = [menu[i] for i in cart_ids if i in menu]
    total = sum(item['price'] for item in cart_items)
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Cart</title><script src="https://cdn.tailwindcss.com"></script></head>
    <body class="bg-orange-50 p-6">
        <div class="max-w-4xl mx-auto">
            <h1 class="text-4xl font-bold mb-8">🛒 Your Cart</h1>
            
            {% if cart_items %}
                <div class="space-y-6">
                    {% for item in cart_items %}
                    <div class="flex items-center justify-between bg-white p-6 rounded-3xl shadow">
                        <div class="flex items-center gap-6">
                            <img src="{{ item.image }}" class="w-28 h-28 object-cover rounded-2xl">
                            <div>
                                <h3 class="font-bold text-2xl">{{ item.name }}</h3>
                                <p class="text-orange-600 text-xl">₹{{ item.price }}</p>
                            </div>
                        </div>
                        <form method="post" action="/remove/{{ item.id }}">
                            <button type="submit" class="text-red-600 hover:text-red-700 font-medium text-lg">Remove</button>
                        </form>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="mt-12 bg-white p-10 rounded-3xl shadow text-center">
                    <p class="text-4xl font-bold">Total: ₹{{ total }}</p>
                    <button onclick="alert('🎉 Order Placed Successfully! Your food will be delivered soon. (Demo)')" 
                            class="mt-8 w-full bg-green-600 text-white py-6 rounded-3xl text-2xl font-semibold">
                        Place Order
                    </button>
                </div>
            {% else %}
                <p class="text-center text-3xl text-gray-500 py-32">Your cart is empty 😢</p>
            {% endif %}
            
            <div class="text-center mt-10">
                <a href="/" class="text-orange-600 text-xl font-medium">← Browse More Food</a>
            </div>
        </div>
    </body>
    </html>
    """, cart_items=cart_items, total=total)

@app.route('/remove/<int:item_id>', methods=['POST'])
def remove_item(item_id):
    if 'cart' in session and item_id in session['cart']:
        session['cart'].remove(item_id)
    return redirect('/cart')

if __name__ == '__main__':
    print("🚀 Online Food Ordering App is Running!")
    print("Open browser → http://127.0.0.1:5000")
    app.run(debug=True)