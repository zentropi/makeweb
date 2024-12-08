from makeweb import App


app = App()


@app.route("/")
def index(request):
    doc = app.html(lang="en")
    with doc:
        with doc.head():
            doc.title("MakeWeb")
        with doc.body():
            doc.h1("Hello, World!")
    return app.response(doc)


if __name__ == "__main__":
    app.run()
