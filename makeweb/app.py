from microdot import Microdot, Response, send_file
from makeweb.html import Html, HtmlFragment


class App(Microdot):
    def response(self, content, status_code=200, headers=None):
        headers = headers or {"Content-Type": "text/html"}
        return Response(content, status_code=status_code, headers=headers)

    def run(self, host="0.0.0.0", port=8000, debug=False, ssl=None):
        print(f"Running on http://localhost:{port}")
        super().run(host=host, port=port, debug=debug, ssl=ssl)
