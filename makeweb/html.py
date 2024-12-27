from .constants import html as html_constants
from textwrap import dedent  # type: ignore
from .sparkline import create_sparkline


class Element:
    def _normalize_attrs(self, attrs):
        normalized = {}
        for key, value in attrs.items():
            norm_key = key.rstrip("_").replace("_", "-")
            if norm_key == "cls":
                norm_key = "class"
            normalized[norm_key] = value
        return normalized

    def __init__(self, tag, parent=None, **attrs):
        if tag in html_constants.deprecated_tags:
            raise ValueError(f"{tag} is deprecated")
        if tag not in html_constants.tags and tag != "html":
            raise ValueError(f"{tag} is not a valid HTML tag")

        self.tag = tag
        self.parent = parent
        self.children = []
        self.attrs = self._normalize_attrs(attrs)
        self.html = (
            parent if isinstance(parent, Html) else parent.html if parent else None
        )

    def __enter__(self):
        if self.tag in html_constants.void_tags:
            raise ValueError(f"{self.tag} is a void tag")
        if self.html:
            self.html.current = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.html:
            self.html.current = (
                self.parent if isinstance(self.parent, Element) else self.html.root
            )
        return False

    def add_child(self, child):
        if isinstance(child, str):
            child = TextNode(child)
        if isinstance(child, HtmlFragment):
            # Add all children from fragment
            for fragment_child in child.root.children:
                fragment_child.parent = self
                self.children.append(fragment_child)
            return child
        if isinstance(child, Element):
            child.parent = self
        self.children.append(child)
        return child

    def _render_atts(self):
        if not self.attrs:
            return ""

        # Split attributes into regular and data-* attributes
        regular_attrs = {
            k: v for k, v in self.attrs.items() if not k.startswith("data-")
        }
        data_attrs = {k: v for k, v in self.attrs.items() if k.startswith("data-")}

        # Handle regular attributes
        sorted_attrs = []
        for k, v in sorted(regular_attrs.items()):
            if isinstance(v, bool):
                if v:  # Only add the attribute name if True
                    sorted_attrs.append(f"{k}")
            elif isinstance(v, list):
                sorted_attrs.append(f'{k}="{" ".join(str(x) for x in v)}"')
            else:
                sorted_attrs.append(f'{k}="{v}"')

        # Handle data attributes (always include value)
        sorted_attrs.extend(f'{k}="{v}"' for k, v in sorted(data_attrs.items()))

        return " " + " ".join(sorted_attrs) if sorted_attrs else ""

    def render(self):
        attrs = self._render_atts()

        if self.tag in html_constants.void_tags:
            return f"<{self.tag}{attrs}/>"

        content = "".join(child.render() for child in self.children)
        return f"<{self.tag}{attrs}>{content}</{self.tag}>"


class TextNode:
    def __init__(self, text):
        self.text = text

    def render(self):
        return str(self.text)


class HtmlBuilder:
    def __init__(self, root_tag, **attrs):
        self.root = Element(root_tag, **attrs)
        self.current = self.root

    def add_child(self, element):
        """Add a child element or fragment directly."""
        if isinstance(element, (Element, HtmlFragment)):
            self.current.add_child(
                element.root if isinstance(element, HtmlBuilder) else element
            )
        else:
            self.current.add_child(element)
        return self

    def __getattr__(self, tag):
        def tag_method(*content, **attrs):
            element = Element(tag, parent=self.current, **attrs)
            element.html = self
            self.current.add_child(element)

            if content:
                element.add_child("".join(map(str, content)))

            return element

        return tag_method

    def markdown(self, text):
        """Render markdown text and add it to the current element"""
        from .markdown import Markdown

        md = Markdown.parse(text)
        self.add_child(md)
        return self

    def sparkline(self, data: list[float], **kwargs):
        """Add a sparkline chart"""
        svg = create_sparkline(data, **kwargs)
        self.current.add_child(svg)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.current = self.root
        return False

    def render(self):
        return self.root.render()

    def __str__(self):
        return self.render()


class Html(HtmlBuilder):
    DOCTYPE = "<!DOCTYPE html>"

    def __init__(self, **attrs):
        super().__init__("html", **attrs)

    def render(self):
        return self.DOCTYPE + super().render()


class HtmlFragment(HtmlBuilder):
    def __init__(self, root_tag=None, **attrs):
        if root_tag is not None and root_tag not in html_constants.tags:
            raise ValueError(f"{root_tag} is not a valid HTML tag")
        if root_tag is None:
            # Create a default wrapper div with fragment class
            super().__init__("div", cls="fragment", **attrs)
        else:
            super().__init__(root_tag, **attrs)

    def render(self):
        return super().render()

    def markdown(self, text):
        # Add dedent before processing markdown
        cleaned_text = dedent(text)
        # Continue with existing markdown processing
        from .markdown import Markdown

        md = Markdown.parse(cleaned_text)
        self.add_child(md)
        return self
