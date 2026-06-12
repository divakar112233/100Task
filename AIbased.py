from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AI Code Generator</title>
<style>
body{
    font-family:Arial;
    background:#f4f4f4;
    padding:20px;
}
.container{
    max-width:900px;
    margin:auto;
    background:white;
    padding:20px;
    border-radius:10px;
}
textarea{
    width:100%;
    height:120px;
}
pre{
    background:#222;
    color:#0f0;
    padding:15px;
    overflow:auto;
}
button{
    padding:10px 20px;
}
</style>
</head>
<body>

<div class="container">
<h1>🤖 AI Code Generator</h1>

<form method="POST">
<textarea name="prompt"
placeholder="Example: Create a Python calculator"></textarea>
<br><br>
<button type="submit">Generate Code</button>
</form>

{% if code %}
<h2>Generated Code</h2>
<pre>{{ code }}</pre>
{% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    code = ""

    if request.method == "POST":
        prompt = request.form["prompt"].lower()

        if "calculator" in prompt:
            code = '''
a = float(input("First Number: "))
b = float(input("Second Number: "))

print("Addition =", a + b)
print("Subtraction =", a - b)
print("Multiplication =", a * b)
print("Division =", a / b)
'''
        elif "hello world" in prompt:
            code = 'print("Hello World")'

        elif "password generator" in prompt:
            code = '''
import random
import string

password = ''.join(
random.choice(string.ascii_letters + string.digits)
for _ in range(12)
)

print(password)
'''
        else:
            code = "# No template found for this request."

    return render_template_string(HTML, code=code)

if __name__ == "__main__":
    app.run(debug=True)