import sys
import time  # type: ignore
from datetime import datetime  # type: ignore

sys.path.append("lib")
from microdot import Microdot, Response, redirect
from makeweb import DictDB

app = Microdot()
db = DictDB("guestbook.db")

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html>
<head>
    <title>Guestbook</title>
    <style>
        body { max-width: 800px; margin: 0 auto; padding: 20px; font-family: sans-serif; }
        .entry { border-bottom: 1px solid #ccc; padding: 10px 0; }
        .entry strong { font-size: 1.2em; }
        .entry p { margin: 5px 0; }
        .entry small { color: #666; }
        form { margin: 20px 0; }
        input, textarea { margin: 5px 0; padding: 5px; width: 100%; }
        button { padding: 10px; }
    </style>
</head>
<body>
    <h1>Guestbook</h1>
    
    <form method="POST" action="/add">
        <input type="text" name="name" placeholder="Your Name" required><br>
        <textarea name="message" placeholder="Your Message" required></textarea><br>
        <button type="submit">Sign Guestbook</button>
    </form>

    <h2>Entries</h2>
    <!--ENTRIES-->
</body>
</html>
"""


@app.route("/")
def index(request):
    entries_html = []
    for key, value in db.items(start_key="0", end_key="999999", incl=True):
        timestamp = time.localtime(value.get('timestamp', 0))
        date_str = f"{timestamp[0]}-{timestamp[1]:02d}-{timestamp[2]:02d} {timestamp[3]:02d}:{timestamp[4]:02d}"
        
        entries_html.insert(
            0,
            f"""
        <div class="entry">
            <strong>{value['name']}</strong>
            <p>{value['message']}</p>
            <small>{date_str}</small>
        </div>
        """,
        )

    return Response(
        HTML_TEMPLATE.replace("<!--ENTRIES-->", "\n".join(entries_html)),
        headers={"Content-Type": "text/html"}
    )


@app.route("/add", methods=["POST"])
def add_entry(request):
    name = request.form.get("name")
    message = request.form.get("message")

    if name and message:
        # Use an incrementing counter for the key
        counter = db.get("counter", 0)
        counter += 1
        # Format counter as 6-digit number for sorting
        key = f"{counter:06d}"
        db["counter"] = counter
        db[key] = {
            "name": name,
            "message": message,
            "timestamp": time.time()
        }

    return redirect("/")


if __name__ == "__main__":
    print("Running guestbook on http://localhost:8000")
    app.run(port=8000)
