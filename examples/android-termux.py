import os
import json
from microdot import Microdot, Response, redirect

app = Microdot()


@app.route("/")
def index(request):
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Torch Control</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Torch Control</h1>
            <form action="/api/torch" method="POST">
                <button type="submit" name="state" value="on">Turn On</button>
                <button type="submit" name="state" value="off">Turn Off</button>
            </form>
            <p><a href="/sms">View SMS Messages</a></p>
        </body>
        </html>
    """
    return Response(body=html, headers={"Content-Type": "text/html"})


@app.route("/api/torch", methods=["POST"])
def torch_control(request):
    state = request.form.get("state")
    if state in ["on", "off"]:
        os.system(f"termux-torch {state}")
        return redirect("/")
    return Response(status=400, body="Invalid state")


@app.route("/sms")
def sms_inbox(request):
    cmd_output = os.popen("termux-sms-list").read()
    # print(cmd_output)
    messages = json.loads(cmd_output)
    
    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>SMS Inbox</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>SMS Inbox</h1>
            <p><a href="/">Back to Torch Control</a></p>
            <table>
                <tr>
                    <th>From</th>
                    <th>Message</th>
                    <th>Received</th>
                </tr>
    """
    
    for msg in messages:
        html += f"""
                <tr>
                    <td>{msg['number']}</td>
                    <td>{msg['body']}</td>
                    <td>{msg['received']}</td>
                </tr>
        """
    
    html += """
            </table>
        </body>
        </html>
    """
    return Response(body=html, headers={"Content-Type": "text/html"})


if __name__ == "__main__":
    print("Running on http://localhost:8000")
    app.run(port=8000)
