from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user == 'admin' and pwd == '1234':
            msg = '✅ Login Success! Welcome ' + user
        else:
            msg = '❌ Invalid Login'
    
    return '''
    <style>
        body{font-family:Arial;background:#667eea;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
        .box{background:white;padding:40px;border-radius:15px;width:300px;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
        h2{text-align:center;color:#667eea}
        input{width:100%;padding:12px;margin:10px 0;border:2px solid #ddd;border-radius:8px;box-sizing:border-box}
        button{width:100%;padding:12px;background:#667eea;color:white;border:none;border-radius:8px;font-size:16px}
        .msg{text-align:center;margin-top:15px;font-weight:bold;color:red}
        .hint{font-size:12px;color:gray;text-align:center;margin-top:15px}
    </style>
    <div class="box">
        <h2>Login 🔐</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button>Login</button>
        </form>
        <div class="msg">''' + msg + '''</div>
        <div class="hint">admin / 1234</div>
    </div>
    '''

app.run(host='0.0.0.0', port=8080)