from makeweb import App, DictDB

app = App()
db = DictDB("todo.db")

def render_todo(todo_id, todo):
    with app.html_fragment("div", cls="todo-item") as item:
        with item.form(method="POST", action=f"/toggle/{todo_id}", cls="toggle-form"):
            item.input(
                type="checkbox",
                checked=todo.get("completed", False),
                onchange="this.form.submit()"
            )
            item.span(todo["text"], cls="todo-text" + (" completed" if todo.get("completed") else ""))
        with item.form(method="POST", action=f"/delete/{todo_id}", cls="delete-form"):
            item.button("Delete", type="submit", cls="delete-btn")
    return item

def render_page(todos):
    doc = app.html(lang="en")
    with doc:
        with doc.head():
            doc.title("Todo List")
            doc.meta(charset="utf-8")
            doc.meta(name="viewport", content="width=device-width, initial-scale=1")
            doc.style("""
                :root { font-size: 16px; }
                * { box-sizing: border-box; }
                body { max-width: 40rem; margin: 0 auto; padding: 1rem; font-family: sans-serif; }
                .todo-form { margin-bottom: 2rem; display: flex; gap: 0.5rem; }
                .todo-input { padding: 0.5rem; flex: 1; }
                .add-btn { padding: 0.5rem 1rem; }
                .todo-item { display: flex; align-items: center; padding: 0.5rem 0; gap: 0.5rem; }
                .toggle-form { flex: 1; display: flex; align-items: center; gap: 0.5rem; }
                .completed { text-decoration: line-through; color: #666; }
                .delete-btn { padding: 0.25rem 0.5rem; background: #ff4444; color: white; border: none; }

                @media (max-width: 480px) {
                    .todo-form { flex-direction: column; }
                    .todo-item { flex-wrap: wrap; }
                    .todo-input, .add-btn, .delete-btn { width: 100%; }
                    .toggle-form { flex: 1 1 auto; min-width: 200px; }
                }
            """)
        with doc.body():
            doc.h1("Todo List")
            
            with doc.form(method="POST", action="/add", cls="todo-form"):
                doc.input(type="text", name="todo", placeholder="Add a new todo", 
                         required=True, cls="todo-input")
                doc.button("Add", type="submit", cls="add-btn")

            for todo_id, todo in todos:
                doc.add_child(render_todo(todo_id, todo))

    return app.response(doc)

@app.route("/")
def index(request):
    todos = sorted(
        [(k, v) for k, v in db.items() if k != "counter"],
        key=lambda x: x[0],
        reverse=True
    )
    return render_page(todos)

@app.route("/add", methods=["POST"])
def add_todo(request):
    todo_text = request.form.get("todo")
    if todo_text:
        counter = db.get("counter", 0)
        counter += 1
        db["counter"] = counter
        db[f"{counter:06d}"] = {"text": todo_text, "completed": False}
    return app.redirect("/")

@app.route("/toggle/<todo_id>", methods=["POST"])
def toggle_todo(request, todo_id):
    if todo_id in db:
        todo = db[todo_id]
        todo["completed"] = not todo.get("completed", False)
        db[todo_id] = todo
    return app.redirect("/")

@app.route("/delete/<todo_id>", methods=["POST"])
def delete_todo(request, todo_id):
    if todo_id in db:
        del db[todo_id]
    return app.redirect("/")

if __name__ == "__main__":
    app.run(port=8000)

