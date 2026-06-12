from flask import Flask, render_template_string
import psutil

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Monitoring Dashboard</title>
    <meta http-equiv="refresh" content="5">
    <style>
        body{
            font-family:Arial;
            background:#f4f4f4;
            padding:20px;
        }
        .container{
            max-width:800px;
            margin:auto;
        }
        .card{
            background:white;
            padding:20px;
            margin:10px 0;
            border-radius:10px;
            box-shadow:0 0 10px #ddd;
        }
        h1{
            text-align:center;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>🌐 Network Monitoring Dashboard</h1>

    <div class="card">
        <h2>Bytes Sent</h2>
        <h3>{{ sent }} MB</h3>
    </div>

    <div class="card">
        <h2>Bytes Received</h2>
        <h3>{{ recv }} MB</h3>
    </div>

    <div class="card">
        <h2>Packets Sent</h2>
        <h3>{{ packets_sent }}</h3>
    </div>

    <div class="card">
        <h2>Packets Received</h2>
        <h3>{{ packets_recv }}</h3>
    </div>

</div>

</body>
</html>
"""

@app.route("/")
def home():
    net = psutil.net_io_counters()

    return render_template_string(
        HTML,
        sent=round(net.bytes_sent / (1024 * 1024), 2),
        recv=round(net.bytes_recv / (1024 * 1024), 2),
        packets_sent=net.packets_sent,
        packets_recv=net.packets_recv
    )

if __name__ == "__main__":
    app.run(debug=True)