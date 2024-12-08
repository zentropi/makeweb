from makeweb import App


app = App()


@app.route("/")
def index(request):
    return app.response("Hello, World!")


if __name__ == "__main__":
    app.run(port=8000)
