from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

internships = [
    {
        "company": "Tech Solutions",
        "role": "Python Intern",
        "location": "Remote"
    },
    {
        "company": "Web World",
        "role": "Frontend Developer Intern",
        "location": "Chennai"
    }
]

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Student Internship Portal</title>
<style>
body{
    font-family:Arial;
    background:#f4f6f9;
    margin:0;
}
.header{
    background:#0d6efd;
    color:white;
    text-align:center;
    padding:20px;
}
.container{
    width:80%;
    margin:auto;
    padding:20px;
}
.card{
    background:white;
    padding:15px;
    margin:15px 0;
    border-radius:10px;
    box-shadow:0 2px 8px rgba(0,0,0,0.2);
}
input{
    width:100%;
    padding:10px;
    margin:8px 0;
}
button{
    background:#0d6efd;
    color:white;
    border:none;
    padding:10px 15px;
    cursor:pointer;
}
</style>
</head>
<body>

<div class="header">
<h1>🎓 Student Internship Portal</h1>
<p>Find and Apply for Internships</p>
</div>

<div class="container">

<h2>Add Internship</h2>

<form method="POST">
<input type="text" name="company" placeholder="Company Name" required>
<input type="text" name="role" placeholder="Internship Role" required>
<input type="text" name="location" placeholder="Location" required>

<button type="submit">Add Internship</button>
</form>

<h2>Available Internships</h2>

{% for job in internships %}
<div class="card">
<h3>{{ job.role }}</h3>
<p><b>Company:</b> {{ job.company }}</p>
<p><b>Location:</b> {{ job.location }}</p>
<button>Apply Now</button>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        internships.append({
            "company": request.form["company"],
            "role": request.form["role"],
            "location": request.form["location"]
        })
        return redirect("/")

    return render_template_string(
        HTML,
        internships=internships
    )

if __name__ == "__main__":
    app.run(debug=True)