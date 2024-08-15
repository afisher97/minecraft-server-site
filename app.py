from flask import Flask, render_template
import os

app = Flask(__name__)


# Path to logs directory
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changelogs')
PERMISSIONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'permissions')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<server>/<file_type>')
def server_file(server, file_type):
    # Determine the file path based on the file type (changelog or permissions)
    if file_type == 'changelog':
        file_path = os.path.join(LOGS_DIR, f'{server}_changelog.txt')
        page_title = f"{server.capitalize()} Changelog"
    elif file_type == 'permissions':
        file_path = os.path.join(PERMISSIONS_DIR, f'{server}_permissions.txt')
        page_title = f"{server.capitalize()} Permissions"
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


if __name__ == '__main__':
    app.run(debug=True)
