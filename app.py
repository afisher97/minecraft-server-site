from flask import Flask, render_template, jsonify
from mcstatus.server import JavaServer
import os
import concurrent.futures

app = Flask(__name__)


# Path to logs directory
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changelogs')
PERMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'permissions')
COMMANDS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commands')

#@app.route('/')
#def home():
#    return render_template('index.html')

@app.route('/<server>/<file_type>')
def server_file(server, file_type):

    # Determine the file path based on the file type
    # If file type changelog, go to changelog directory and look for servername_changelog
    if file_type == 'changelog':
        file_path = os.path.join(LOGS_DIR, f'{server}_changelog.txt')
        page_title = f"{server.capitalize()} Changelog"

    # If file type permissions, go to changelog directory and look for servername_permissions
    elif file_type == 'permissions':
        file_path = os.path.join(PERMISSIONS_DIR, f'{server}_permissions.txt')
        page_title = f"{server.capitalize()} Permissions"

    # If file type commands, go to changelog directory and look for servername_commands
    elif file_type == 'commands':
        file_path = os.path.join(COMMANDS_DIR, f'{server}_commands.txt')
        page_title = f"{server.capitalize()} Commands"

    # File must not exist
    else:
        return "File type not found", 404

    # Read the file contents
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
    except FileNotFoundError:
        return "File not found", 404

    # Render the same template with dynamic content
    return render_template('server_file.html', title=page_title, content=content)


def query_minecraft_server(ip, port, timeout=1.0):
    try:
        # Create the server object (this call should be fast)
        server = JavaServer.lookup(f"{ip}:{port}")

        # Use a ThreadPoolExecutor to enforce a timeout on the blocking call
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(server.status)  # server.status() without a timeout argument
            status = future.result(timeout=timeout)   # enforce timeout here

        return {
            "version": status.version.name,
            "players_online": status.players.online,
            "latency": status.latency,
            "players_sample": [player.name for player in status.players.sample] if status.players.sample else [],
            "error": False
        }
    except concurrent.futures.TimeoutError:
        print(f"Timeout querying {ip}:{port}")
        return {
            "version": "Unknown",
            "players_online": 0,
            "latency": None,
            "players_sample": [],
            "error": True
        }
    except Exception as e:
        print(f"Error querying {ip}:{port}: {e}")
        return {
            "version": "Unknown",
            "players_online": 0,
            "latency": None,
            "players_sample": [],
            "error": True
        }

@app.route('/server/<server_ip>')
def server_status(server_ip):
    server_info = query_minecraft_server(server_ip)
    return render_template('server_status.html', server_info=server_info)


@app.route('/api/server_status/<server_name>')
def get_server_status(server_name):
    # Map server names to IP/port
    servers = {
        "buildcraft": ("mc1.averyfisher.com", 25565),
        "savagelands": ("mc2.averyfisher.com", 25566),
    }

    ip_port = servers.get(server_name)
    if not ip_port:
        return jsonify({"error": True, "message": "Unknown server"}), 404

    ip, port = ip_port
    result = query_minecraft_server(ip, port)
    print(result)
    return jsonify(result)

@app.route('/dynmap/<server_ip>')
def dynmap(server_ip):
    # Pass the server IP to the dynmap.html template
    dynmap_url = f'http://{server_ip}:8123/'
    return render_template('dynmap.html', dynmap_url=dynmap_url)


@app.route('/')
def home():
    # Render the page with placeholders
    return render_template('index.html')

@app.route("/test")
# Test route to check network performace
def test():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
