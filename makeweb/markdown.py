from io import StringIO
from .html import Element, HtmlFragment
from udownmark import Markdown as Udownmark

class Markdown:
    @staticmethod
    def parse(text):
        output = StringIO()
        md = Udownmark(output)
        md.render(text.splitlines())
        html = output.getvalue()
        
        # Create a fragment to hold the markdown content
        fragment = HtmlFragment("div", cls="markdown")
        # Add the raw HTML content
        fragment.add_child(html)
        return fragment