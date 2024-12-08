import unittest
from makeweb.html import Html, HtmlFragment

DOCTYPE = "<!DOCTYPE html>"


class TestHtml(unittest.TestCase):
    def test_basic_tags(self):
        doc = Html()
        self.assertEqual(str(doc), DOCTYPE + "<html></html>")

    def test_nested_tags(self):
        doc = Html()
        with doc.div(cls="container"):
            doc.p("nested")
        self.assertEqual(
            str(doc),
            DOCTYPE + '<html><div class="container"><p>nested</p></div></html>',
        )

    def test_deprecated_tag(self):
        doc = Html()
        with self.assertRaises(ValueError) as cm:
            doc.blink()
        self.assertEqual(str(cm.exception), "blink is deprecated")

    def test_deeply_nested_tags(self):
        doc = Html()
        with doc.div(id="level1"):
            with doc.section(cls="level2"):
                with doc.article(id="level3"):
                    with doc.div(cls="level4"):
                        doc.p("deeply nested")
        self.assertEqual(
            str(doc),
            DOCTYPE
            + '<html><div id="level1"><section class="level2"><article id="level3">'
            + '<div class="level4"><p>deeply nested</p></div>'
            + "</article></section></div></html>",
        )

    def test_invalid_tag(self):
        doc = Html()
        with self.assertRaises(ValueError) as cm:
            doc.invalidtag()
        self.assertEqual(str(cm.exception), "invalidtag is not a valid HTML tag")

    def test_void_tag_nesting(self):
        doc = Html()
        with self.assertRaises(ValueError) as cm:
            with doc.img(src="image.jpg"):
                doc.p("this shouldn't work")
        self.assertEqual(str(cm.exception), "img is a void tag")

    def test_attributes_normalization(self):
        doc = Html()
        with doc.div(cls_="test", data_value="123"):
            pass
        self.assertEqual(
            str(doc), DOCTYPE + '<html><div class="test" data-value="123"></div></html>'
        )

    def test_attributes_normalization_variations(self):
        doc = Html()
        with doc.div(
            cls_="main",  # trailing underscore
            data_test="1",  # data attribute
            aria_label="test",  # aria attribute
            my_attr_name="val",  # multiple underscores
            class_="ignored",  # cls has precedence over class_
        ):
            pass
        self.assertEqual(
            str(doc),
            DOCTYPE
            + '<html><div aria-label="test" class="main" my-attr-name="val" data-test="1"></div></html>',
        )

    def test_empty_attributes(self):
        doc = Html()
        with doc.div():
            pass
        self.assertEqual(str(doc), DOCTYPE + "<html><div></div></html>")

    def test_document_attributes(self):
        doc = Html(lang="en", data_theme="dark")
        self.assertEqual(
            str(doc), DOCTYPE + '<html lang="en" data-theme="dark"></html>'
        )

    def test_empty_content(self):
        doc = Html()
        doc.p()
        self.assertEqual(str(doc), DOCTYPE + "<html><p></p></html>")

    def test_multiple_content_items(self):
        doc = Html()
        doc.p("Hello", " ", "World", "!")
        self.assertEqual(str(doc), DOCTYPE + "<html><p>Hello World!</p></html>")

    def test_void_tag_self_closing(self):
        doc = Html()
        doc.img(alt="Test", src="test.jpg")  # Match alphabetical order in test
        self.assertEqual(
            str(doc), DOCTYPE + '<html><img alt="Test" src="test.jpg"/></html>'
        )

    def test_nested_content_mixing(self):
        doc = Html()
        with doc.div():
            doc.span("inline")
            with doc.p():
                doc.em("emphasized")
            doc.span("more")
        self.assertEqual(
            str(doc),
            DOCTYPE
            + "<html><div><span>inline</span><p><em>emphasized</em></p><span>more</span></div></html>",
        )

    def test_attribute_rendering_order(self):
        doc = Html()
        with doc.div(
            style="color: red", id="test", cls="main", data_value="1", data_attr="2"
        ):
            pass
        self.assertEqual(
            str(doc),
            DOCTYPE
            + '<html><div class="main" id="test" style="color: red" data-attr="2" data-value="1"></div></html>',
        )

    def test_boolean_attributes(self):
        doc = Html()
        with doc.div(hidden=True, data_expanded=False):
            pass
        self.assertEqual(
            str(doc), DOCTYPE + '<html><div hidden data-expanded="False"></div></html>'
        )

    def test_mixed_attribute_types(self):
        doc = Html()
        with doc.div(id=1, cls=["a", "b"], data_count=42):
            pass
        self.assertEqual(
            str(doc),
            DOCTYPE + '<html><div class="a b" id="1" data-count="42"></div></html>',
        )

    def test_html_fragment_invalid_root(self):
        with self.assertRaises(ValueError) as cm:
            HtmlFragment("invalid")
        self.assertEqual(str(cm.exception), "invalid is not a valid HTML tag")

    def test_html_fragment_nested(self):
        frag = HtmlFragment("section", id="main")
        with frag.article(cls="content"):
            with frag.div():
                frag.p("Test")
        self.assertEqual(
            str(frag),
            '<section id="main"><article class="content"><div><p>Test</p></div></article></section>',
        )

    def test_html_multiple_root_children(self):
        doc = Html()
        with doc:
            doc.header(id="header")
            with doc.main():
                doc.p("content")
            doc.footer(cls="bottom")
        self.assertEqual(
            str(doc),
            DOCTYPE
            + '<html><header id="header"></header><main><p>content</p></main><footer class="bottom"></footer></html>',
        )

    def test_html_context_manager(self):
        doc = Html()
        with doc:
            doc.div("first")
        with doc:
            doc.div("second")
        self.assertEqual(
            str(doc), DOCTYPE + "<html><div>first</div><div>second</div></html>"
        )

    def test_html_fragment_as_content(self):
        doc = Html()
        frag = HtmlFragment("nav")
        with frag:
            frag.a("Link", href="#")

        with doc:
            with doc.header():
                doc.add_child(frag)
            doc.main("Content")

        self.assertEqual(
            str(doc),
            DOCTYPE
            + '<html><header><nav><a href="#">Link</a></nav></header><main>Content</main></html>',
        )

    def test_html_fragment_no_root(self):
        frag = HtmlFragment()
        with frag:
            frag.p("First")
            frag.p("Second")
        self.assertEqual(str(frag), '<div class="fragment"><p>First</p><p>Second</p></div>')

    def test_html_fragment_nested_no_root(self):
        frag = HtmlFragment()
        with frag:
            with frag.div():
                frag.p("Test")
            frag.span("More")
        self.assertEqual(str(frag), '<div class="fragment"><div><p>Test</p></div><span>More</span></div>')

    def test_html_fragment_as_content_no_root(self):
        doc = Html()
        frag = HtmlFragment()
        with frag:
            frag.a("Link 1", href="#1")
            frag.a("Link 2", href="#2")

        with doc:
            with doc.nav():
                doc.add_child(frag)

        self.assertEqual(
            str(doc),
            DOCTYPE + '<html><nav><div class="fragment"><a href="#1">Link 1</a><a href="#2">Link 2</a></div></nav></html>'
        )


if __name__ == "__main__":
    unittest.main()
