from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# ===== உன் Gmail Details இங்க மாத்து =====
SENDER = "yourgmail@gmail.com"           # உன் Gmail ID
APP_PASSWORD = "abcdefghijklmnop"        # Gmail App Password 16 எழுத்து
RECEIVER = "yourgmail@gmail.com"         # Message எங்க வரணுமோ
# =========================================

HTML_FORM = '''
<!doctype html>
<html>
<head>
<title>Contact Form</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
<style>
body{font-family:Arial;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;justify-content:center;align-items:center;min-height:100vh;margin:0;padding:20px}
.box{background:white;padding:30px;border-radius:15px;width:100%;max-width:380px;box-shadow:0 10px 30px rgba(0,0,0,0.3)}
h2{text-align:center;color:#667eea;margin:0 0 20px}
input,textarea{width:100%;padding:12px;margin:8px 0;border:2px solid #ddd;border-radius:8px;box-sizing:border-box;font-size:14px}
input:focus,textarea:focus{border-color:#667eea;outline:none}
textarea{height:120px;resize:vertical}
button{width:100%;padding:14px;background:#667eea;color:white;border:none;border-radius:8px;font-size:16px;font-weight:bold;margin-top:10px;cursor:pointer}
button:hover{background:#5568d3}
.msg{text-align:center;margin-top:15px;padding:10px;border-radius:8px;font-weight:bold}
.success{background:#d4edda;color:#155724}
.error{background:#f8d7da;color:#721c24}
</style>
<div class="box">
<h2>Contact Us</h2>
<form method="POST">
<input name="name" placeholder="Your Name" required>
<input type="email" name="email" placeholder="Your Email" required>
<input name="subject" placeholder="Subject" required>
<textarea name="message" placeholder="Your Message" required></textarea>
<button>Send Message</button>
</form>
{{msg|safe}}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def contact():
    msg = ''
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        subject = request.form['subject'].strip()
        message = request.form['message'].strip()
        
        # Validation
        if len(name) < 3:
            msg = '<div class="msg error">Name 3 letters minimum</div>'
        elif '@' not in email:
            msg = '<div class="msg error">Valid Email குடு</div>'
        elif len(message) < 10:
            msg = '<div class="msg error">Message 10 letters minimum</div>'
        else:
            try:
                # Email Body
                body = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message}"
                
                mail = MIMEText(body)
                mail['Subject'] = f"Contact: {subject}"
                mail['From'] = SENDER
                mail['To'] = RECEIVER
                mail['Reply-To'] = email
                
                # Send via Gmail SMTP
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(SENDER, APP_PASSWORD)
                server.sendmail(SENDER, RECEIVER, mail.as_string())
                server.quit()
                
                msg = '<div class="msg success">Message Sent Successfully! Check your Gmail Inbox</div>'
            except Exception as e:
                msg = '<div class="msg error">Error: App Password Check பண்ணு</div>'
    
    return render_template_string(HTML_FORM, msg=msg)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)