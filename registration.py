from flask import Flask, request
app = Flask(__name__)

users = {}

def page(box_content):
    return (
        "<style>"
        "body{font-family:Arial;background:#667eea;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}"
        ".box{background:white;padding:35px;border-radius:15px;width:320px}"
        "h2{text-align:center;color:#667eea}"
        "input{width:100%;padding:12px;margin:8px 0;border:2px solid #ddd;border-radius:8px;box-sizing:border-box}"
        "button{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:8px;font-size:16px}"
        ".link{text-align:center;margin-top:15px}"
        "a{color:#667eea;text-decoration:none;font-weight:bold}"
        "</style>"
        + box_content
    )

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user in users and users[user] == pwd:
            msg = '<div style="color:green;text-align:center;font-weight:bold">✅ Welcome ' + user + '!</div>'
        else:
            msg = '<div style="color:red;text-align:center;font-weight:bold">❌ Wrong Login</div>'

    content = '<div class="box"><h2>Login 🔐</h2><form method="POST"><input name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><button>Login</button></form>' + msg + '<div class="link">New User? <a href="/register">Register Here</a></div></div>'
    return page(content)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        email = request.form['email']
        if user in users:
            msg = '<div style="color:red;text-align:center;font-weight:bold">❌ Username Exists!</div>'
        else:
            users[user] = pwd
            msg = '<div style="color:green;text-align:center;font-weight:bold">✅ Registration Success!</div>'

    content = '<div class="box"><h2>Register 📝</h2><form method="POST"><input name="username" placeholder="Username" required><input type="email" name="email" placeholder="Email" required><input type="password" name="password" placeholder="Password" required><button>Register</button></form>' + msg + '<div class="link">Already Have Account? <a href="/">Login Here</a></div></div>'
    return page(content)

app.run(host='0.0.0.0', port=8080)