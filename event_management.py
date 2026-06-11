from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

events = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Event Management System</title>
    <style>
        body{
            font-family: Arial;
            background:#f4f4f4;
            margin:0;
        }

        .header{
            background:#4CAF50;
            color:white;
            text-align:center;
            padding:20px;
        }

        .container{
            width:80%;
            margin:auto;
            padding:20px;
        }

        form{
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0 0 10px lightgray;
        }

        input{
            width:100%;
            padding:10px;
            margin:10px 0;
        }

        button{
            background:#4CAF50;
            color:white;
            border:none;
            padding:10px 20px;
            cursor:pointer;
        }

        .event{
            background:white;
            margin-top:15px;
            padding:15px;
            border-radius:10px;
            box-shadow:0 0 5px gray;
        }
    </style>
</head>
<body>

<div class="header">
    <h1>🎉 Event Management System</h1>
</div>

<div class="container">

<form method="POST">
    <input type="text" name="name" placeholder="Event Name" required>

    <input type="date" name="date" required>

    <input type="text" name="location" placeholder="Location" required>

    <button type="submit">Add Event</button>
</form>

<h2>Upcoming Events</h2>

{% for event in events %}
<div class="event">
    <h3>{{ event.name }}</h3>
    <p><b>Date:</b> {{ event.date }}</p>
    <p><b>Location:</b> {{ event.location }}</p>
</div>
{% endfor %}

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        events.append({
            "name": request.form["name"],
            "date": request.form["date"],
            "location": request.form["location"]
        })
        return redirect("/")

    return render_template_string(HTML, events=events)

if __name__ == "__main__":
    app.run(debug=True)