from makeweb import App

app = App()
app.host = "0.0.0.0"
app.port = 8000
app.debug = True
app.db = "snippets.db"


@app.route("/")
def index(request):
    doc = app.html()
    with doc:
        with doc.head():
            doc.title("Snippets")
        with doc.body():
            doc.h1("Snippets")
            with doc.ul():
                for key, value in app.db.items():
                    with doc.li():
                        doc.h3(key)
                        doc.pre(value)
    return app.response(doc)


app.run()
