from makeweb import App

app = App()
app.host = "0.0.0.0"
app.port = 8000
app.debug = True
app.db = "snippets.db"


@app.component(tag="section")
def snippets(doc, _request):
    with doc:
        for key, value in app.db.items():
            with doc.div():
                doc.h3(key)
                doc.pre(value)


@app.component(tag="section")
def snippet_form(doc, _request):
    with doc.form(action="/snippets/add", method="post"):
        doc.input(type="text", name="name", placeholder="Name")
        doc.textarea(name="value", placeholder="Value")
        doc.input(type="submit", value="Add")


@app.page("/")
def index(doc, request):
    with doc:
        with doc.head():
            doc.meta(charset="utf-8")
            doc.title("Snippets")
            doc.style(
                """
                body { 
                    font-family: sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                form {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    margin-bottom: 2rem;
                }
                input[type="text"], textarea {
                    padding: 8px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                }
                textarea {
                    min-height: 100px;
                }
                input[type="submit"] {
                    background: #007bff;
                    color: white;
                    border: none;
                    padding: 10px;
                    border-radius: 4px;
                    cursor: pointer;
                }
                input[type="submit"]:hover {
                    background: #0056b3;
                }
            """
            )
        with doc.body():
            doc.h1("Snippets")
            doc.add_child(snippet_form(doc, request))
            doc.add_child(snippets(doc, request))


@app.route("/snippets/add", methods=["post"])
def add_snippet(request):
    name = request.form.get("name")
    value = request.form.get("value")
    app.db[name] = value
    return app.redirect("/")


app.run()
