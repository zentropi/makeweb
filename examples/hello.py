import sys

sys.path.append("lib")
from microdot import Microdot, Response


app = Microdot()


@app.route("/")
def index(request):
    return Response("Hello, World!")


if __name__ == "__main__":
    print("Running on http://localhost:8000")
    app.run(port=8000)
