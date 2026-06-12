from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Reels Platform</title>
<style>
body{
    margin:0;
    background:black;
    color:white;
    font-family:Arial;
    display:flex;
    justify-content:center;
}
.container{
    width:400px;
    height:100vh;
    overflow-y:scroll;
    scroll-snap-type:y mandatory;
}
.reel{
    height:100vh;
    scroll-snap-align:start;
}
video{
    width:100%;
    height:100%;
    object-fit:cover;
}
</style>
</head>
<body>

<div class="container">

<div class="reel">
<video controls autoplay loop>
<source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4">
</video>
</div>

<div class="reel">
<video controls loop>
<source src="https://www.w3schools.com/html/movie.mp4" type="video/mp4">
</video>
</div>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)