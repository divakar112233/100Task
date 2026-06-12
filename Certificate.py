from flask import Flask, request, render_template_string

app = Flask(__name__)

certificates = {
    "CERT001": {
        "name": "Dhiva",
        "course": "Python Programming",
        "date": "12-06-2026"
    },
    "CERT002": {
        "name": "John",
        "course": "Web Development",
        "date": "10-06-2026"
    },
    "CERT003": {
        "name": "David",
        "course": "Data Science",
        "date": "05-06-2026"
    }
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Certificate Verification System</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg,#4facfe,#00f2fe);
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            margin:0;
        }

        .container{
            background:white;
            padding:30px;
            width:500px;
            border-radius:15px;
            box-shadow:0 5px 15px rgba(0,0,0,0.3);
            text-align:center;
        }

        h1{
            color:#333;
        }

        input{
            width:80%;
            padding:12px;
            border:1px solid #ccc;
            border-radius:5px;
            margin:10px 0;
        }

        button{
            padding:12px 25px;
            background:#28a745;
            color:white;
            border:none;
            border-radius:5px;
            cursor:pointer;
        }

        button:hover{
            background:#218838;
        }

        .valid{
            color:green;
            font-weight:bold;
        }

        .invalid{
            color:red;
            font-weight:bold;
        }

        .result{
            margin-top:20px;
            padding:15px;
            background:#f8f9fa;
            border-radius:10px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>Certificate Verification System</h1>

    <form method="POST">
        <input type="text" name="cert_id"
        placeholder="Enter Certificate ID (e.g. CERT001)" required>
        <br>
        <button type="submit">Verify Certificate</button>
    </form>

    {% if result %}
    <div class="result">

        {% if result.status == "VALID" %}
            <h2 class="valid">✓ Certificate Verified</h2>

            <p><b>Certificate ID:</b> {{ cert_id }}</p>
            <p><b>Name:</b> {{ result.name }}</p>
            <p><b>Course:</b> {{ result.course }}</p>
            <p><b>Issue Date:</b> {{ result.date }}</p>
            <p class="valid">Status : VALID</p>

        {% else %}
            <h2 class="invalid">✗ Certificate Not Found</h2>
            <p class="invalid">Status : INVALID</p>
        {% endif %}

    </div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    cert_id = ""

    if request.method == "POST":
        cert_id = request.form["cert_id"].upper()

        if cert_id in certificates:
            result = certificates[cert_id]
            result["status"] = "VALID"
        else:
            result = {"status": "INVALID"}

    return render_template_string(
        HTML,
        result=result,
        cert_id=cert_id
    )

if __name__ == "__main__":
    app.run(debug=True)