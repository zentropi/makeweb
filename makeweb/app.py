from microdot import Microdot, Response, send_file, redirect
from makeweb.html import Html, HtmlFragment
from makeweb.dictdb import DictDB

class App(Microdot):
    def __init__(self, host="0.0.0.0", port=8000, debug=False, db=None):
        super().__init__()
        self.host = host
        self.port = port
        self.debug = debug
        self._db = None
        self.db = db

    @property
    def db(self):
        return self._db

    @db.setter
    def db(self, value):
        if isinstance(value, str):
            self._db = DictDB(value)
        else:
            self._db = value

    def response(self, content, status_code=200, headers=None, reason=None):
        """Create a new response."""
        headers = headers or {"Content-Type": "text/html"}
        if isinstance(content, Html):
            content = content.render()
        return Response(
            content, status_code=status_code, headers=headers, reason=reason
        )
    
    def send_file(self, path, **kwargs):
        """Send a file."""
        return send_file(path, **kwargs)
    
    def redirect(self, location, status_code=302):
        """Redirect to a new location."""
        return redirect(location, status_code=status_code)

    def html(self, **attrs):
        """Create a new HTML document."""
        return Html(**attrs)

    def html_fragment(self, tag, **attrs):
        """Create a new HTML fragment."""
        return HtmlFragment(tag, **attrs)
    
    def run(self, host=None, port=None, debug=None, ssl=None):
        """Run the application."""
        run_host = host if host is not None else self.host
        run_port = port if port is not None else self.port
        run_debug = debug if debug is not None else self.debug
        
        print(f"Running on http://{run_host}:{run_port}")
        super().run(host=run_host, port=run_port, debug=run_debug, ssl=ssl)
