from flask import Flask, render_template
import os

app = Flask(__name__)


# Path to logs directory
LOGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changelogs')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/changelog_buildcraft')
def changelog_buildcraft():
    # Read the changelog file
    changelog_file = os.path.join(LOGS_DIR, 'buildcraft_changelog.txt')
    with open(changelog_file, 'r') as file:
        changelog = file.readlines()

    return render_template('changelog_buildcraft.html', changelog=changelog)


if __name__ == '__main__':
    app.run(debug=True)
