import os

from microdot import Microdot, Response


class TailscalePeer:
    def __init__(self, ip, name, user, os, status):
        self.ip = ip
        self.name = name
        self.user = user
        self.os = os
        self.status = status


def get_status():
    try:
        output = os.popen("tailscale status").read()
        peers = []
        for line in output.strip().split("\n"):
            if not line:
                continue
            parts = line.split(None, 4)
            if len(parts) >= 4:
                ip, name, user, os_name = parts[:4]
                status = parts[4] if len(parts) > 4 else "-"
                peers.append(TailscalePeer(ip, name, user, os_name, status))
        return peers
    except Exception as e:
        print(f"Error getting tailscale status: {e}")
        return []


app = Microdot()


@app.route("/")
async def index(request):
    peers = sorted(get_status(), key=lambda x: x.name.lower())
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tailscale Status</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h1>Tailscale Peers</h1>
        <table>
            <tr>
                <th>IP</th>
                <th>Name</th>
                <th>User</th>
                <th>OS</th>
                <th>Status</th>
            </tr>
    """
    for peer in peers:
        html += f"""
            <tr>
                <td>{peer.ip}</td>
                <td>{peer.name}</td>
                <td>{peer.user}</td>
                <td>{peer.os}</td>
                <td>{peer.status}</td>
            </tr>
        """
    html += """
        </table>
    </body>
    </html>
    """
    return Response(html, headers={"Content-Type": "text/html"})


if __name__ == "__main__":
    print("Running on http://localhost:8000")
    app.run(port=8000)
