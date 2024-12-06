import sys

sys.path.append("lib")
from microdot import Microdot


app = Microdot()


@app.route("/")
def index(request):
    return "Hello, World!"


if __name__ == "__main__":
    print("Running on http://localhost:5000")
    app.run(port=5000)
