from flask import Flask

# Create Flask app instance
app = Flask(__name__)

# Define route for home page
@app.route('/')
def hello_world():
    return '<h1>Hello, World! 👋</h1><p>Welcome to your first Flask app.</p>'

# Optional: Add another route
@app.route('/about')
def about():
    return '<h1>About Page</h1><p>This is a simple Flask Hello World app.</p>'

if __name__ == '__main__':
    print("🚀 Starting Flask Hello World App...")
    print("Open browser → http://127.0.0.1:5000")
    app.run(debug=True, port=5000)