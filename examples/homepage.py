from microdot import Microdot, Response, send_file
from makeweb.html import Html, HtmlFragment

app = Microdot()


def make_navigation():
    with HtmlFragment("nav", cls="toolbar") as nav:
        nav.style("nav a { margin-right: 0.75rem; }")
        nav.a("Home", href="/")
        nav.span("&nbsp;")
        nav.a("Social", href="/social")
    return nav


def home_content():
    with HtmlFragment("section", cls="content") as section:
        section.markdown(
            """
            ## Welcome

            Example of a homepage using Microdot and MakeWeb.
            """
        )
    return section


def social_content():
    with HtmlFragment("section", cls="content") as section:
        section.markdown(
            """
            ## Fediverse

            - [example@example.social](https://example.social/@example)
            """
        )
    return section


def template_page(title, content):
    doc = Html(lang="en")
    with doc:
        with doc.head():
            doc.title(title)
            doc.meta(charset="utf-8")
            doc.meta(name="viewport", content="width=device-width, initial-scale=1")
            doc.style(
                """
                /* Reset box sizing */
                * {
                    box-sizing: border-box;
                }

                html {
                    font-size: 16px;
                }
                """
            )
            doc.link(rel="prefetch", href="projects")
            doc.link(rel="prefetch", href="social")
        with doc.body():
            doc.add_child(make_navigation())
            with doc.main():
                doc.h1(title)
                doc.add_child(content)
    return Response(doc.render(), headers={"Content-Type": "text/html"})


@app.route("/")
async def index(request):
    return template_page("Home", home_content())


@app.route("/social")
async def projects(request):
    return template_page("Social", social_content())


if __name__ == "__main__":
    print("Running on http://localhost:8000")
    app.run(port=8000, debug=True)
