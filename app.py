from flask import Flask, render_template
from mcstatus.server import JavaServer
import os

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


def query_minecraft_server(ip, port=25565):
    try:
        server = JavaServer.lookup(f"{ip}:{port}")
        status = server.status()

        # Return the server information
        server_info = {
            "version": status.version.name,
            "players_online": status.players.online,
            "latency": status.latency,
            "players_sample": [player.name for player in status.players.sample] if status.players.sample else []
        }
        return server_info
    except Exception as e:

        # In case the server is offline or can't be reached
        return {"error": str(e)}

@app.route('/server/<server_ip>')
def server_status(server_ip):
    server_info = query_minecraft_server(server_ip)
    return render_template('server_status.html', server_info=server_info)

@app.route('/dynmap/<server_ip>')
def dynmap(server_ip):
    # Pass the server IP to the dynmap.html template
    dynmap_url = f'http://{server_ip}:8123/'
    return render_template('dynmap.html', dynmap_url=dynmap_url)


@app.route('/')
def home():
    # Query BuildCraft server stats
    buildcraft_info = query_minecraft_server("50.86.215.18", 25565)
    # Similarly, query other servers if needed
    return render_template('index.html', buildcraft_info=buildcraft_info)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
