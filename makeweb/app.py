from microdot import Microdot, Response, send_file
from makeweb.html import Html, HtmlFragment


class App(Microdot):
    def response(self, content, status_code=200, headers=None, reason=None):
        """Create a new response."""
        headers = headers or {"Content-Type": "text/html"}
        if isinstance(content, Html):
            content = content.render()
        return Response(
            content, status_code=status_code, headers=headers, reason=reason
        )

    def html(self, **attrs):
        """Create a new HTML document."""
        return Html(**attrs)

    def html_fragment(self, tag, **attrs):
        """Create a new HTML fragment."""
        return HtmlFragment(tag, **attrs)

    def run(self, host="0.0.0.0", port=8000, debug=False, ssl=None):
        """Run the application."""
        print(f"Running on http://localhost:{port}")
        super().run(host=host, port=port, debug=debug, ssl=ssl)
