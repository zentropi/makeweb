#!~/bin/makeweb
from makeweb import App, DictDB

app = App()
app.host = "0.0.0.0"
app.port = 8022
app.debug = True
app.db = DictDB("weather.db")


@app.page("/")
def index(doc, _request):
    with doc.head():
        doc.title("Weather")
        doc.inline("style", "styles.css")
    with doc.body():
        doc.h1("Weather")


app.run()
