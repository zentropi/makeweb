import time  # type: ignore
from makeweb import App, DictDB

app = App()
db = DictDB("guestbook.db")


def render_entry(timestamp, name, message):
    date_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))
    with app.html_fragment("div", cls="entry") as entry:
        entry.strong(name)
        entry.p(message)
        with entry.small():
            entry.time(date_str, datetime=str(timestamp))
    return entry


def render_page(entries):
    doc = app.html(lang="en")
    with doc:
        with doc.head():
            doc.title("Guestbook")
            doc.style(
                """
                :root { font-size: 16px; }
                * { box-sizing: border-box; }
                body { max-width: 46rem; margin: 0 auto; padding: 2rem; font-family: sans-serif; }
                .entry { border-bottom: 1px solid #ccc; padding: 1rem 0; }
                .entry strong { font-size: 1.2rem; }
                .entry p { margin: 1rem 0; }
                .entry small { color: #666; }
                form { margin: 3rem 0; }
                input, textarea { margin: 1rem 0; padding: .75rem; width: 100%; }
                textarea { min-height: 8rem; }
                button { padding: 1rem; margin: 1rem 0; background-color: #007bff; color: white; border: none; }
            """
            )
        with doc.body():
            doc.h1("Guestbook")

            with doc.form(method="POST", action="/add"):
                doc.input(
                    type="text", name="name", placeholder="Your Name", required=True
                )
                doc.br()
                doc.textarea(name="message", placeholder="Your Message", required=True)
                doc.br()
                doc.button("Sign Guestbook", type="submit")

            doc.h2("Entries")
            for entry in entries:
                doc.add_child(entry)

    return app.response(doc)


@app.route("/")
def index(request):
    entries = []
    for _key, value in db.items(start_key="0", end_key="999999", incl=True):
        entry = render_entry(value.get("timestamp", 0), value["name"], value["message"])
        entries.insert(0, entry)

    return render_page(entries)


@app.route("/add", methods=["POST"])
def add_entry(request):
    name = request.form.get("name")
    message = request.form.get("message")

    if name and message:
        counter = db.get("counter", 0)
        counter += 1
        key = f"{counter:06d}"
        db["counter"] = counter
        db[key] = {"name": name, "message": message, "timestamp": time.time()}

    return app.redirect("/")


if __name__ == "__main__":
    app.run(port=8000)
