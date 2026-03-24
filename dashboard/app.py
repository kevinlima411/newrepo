import os
import base64
import requests
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'kevin-bot-dashboard')

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO_OWNER = 'kevinlima411'
REPO_NAME = 'newrepo'
DEFAULT_BRANCH = 'main'

API_BASE = 'https://api.github.com'


def headers():
    return {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json',
    }


def gh_get(path, params=None):
    r = requests.get(f'{API_BASE}{path}', headers=headers(), params=params, timeout=10)
    r.raise_for_status()
    return r.json()


AGENT_STATUS = [
    {'name': 'Cleaning Agent', 'domain': 'DK client SMS', 'status': 'active', 'phase': 1},
    {'name': 'Flooring Intel', 'domain': 'Contractor leads', 'status': 'planned', 'phase': 2},
    {'name': 'Finance Agent', 'domain': 'Personal finance', 'status': 'planned', 'phase': 3},
    {'name': 'Personal Agent', 'domain': 'Life & family', 'status': 'planned', 'phase': 4},
]


@app.route('/')
def index():
    commits = gh_get(f'/repos/{REPO_OWNER}/{REPO_NAME}/commits', params={'per_page': 5})
    repo = gh_get(f'/repos/{REPO_OWNER}/{REPO_NAME}')
    return render_template('index.html', commits=commits, repo=repo, agents=AGENT_STATUS)


@app.route('/files')
@app.route('/files/<path:filepath>')
def files(filepath=''):
    contents = gh_get(f'/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}')
    if isinstance(contents, list):
        contents.sort(key=lambda x: (x['type'] != 'dir', x['name'].lower()))
        return render_template('files.html', items=contents, current_path=filepath)
    else:
        content = base64.b64decode(contents['content']).decode('utf-8')
        return render_template('file_view.html', file=contents, content=content, current_path=filepath)


@app.route('/files/<path:filepath>/edit', methods=['GET', 'POST'])
def file_edit(filepath):
    if request.method == 'POST':
        new_content = request.form['content']
        message = request.form.get('message', f'Update {filepath} via dashboard').strip()
        sha = request.form['sha']

        encoded = base64.b64encode(new_content.encode('utf-8')).decode('utf-8')
        payload = {
            'message': message or f'Update {filepath} via dashboard',
            'content': encoded,
            'sha': sha,
            'branch': DEFAULT_BRANCH,
        }
        r = requests.put(
            f'{API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}',
            headers=headers(),
            json=payload,
            timeout=10,
        )
        if r.status_code in (200, 201):
            flash('Saved.', 'success')
            return redirect(url_for('files', filepath=filepath))
        else:
            flash(f'Error: {r.json().get("message", "Unknown")}', 'error')

    contents = gh_get(f'/repos/{REPO_OWNER}/{REPO_NAME}/contents/{filepath}')
    content = base64.b64decode(contents['content']).decode('utf-8')
    return render_template('file_edit.html', file=contents, content=content, current_path=filepath)


@app.route('/commits')
def commits():
    data = gh_get(f'/repos/{REPO_OWNER}/{REPO_NAME}/commits', params={'per_page': 25})
    return render_template('commits.html', commits=data)


@app.route('/issues')
def issues():
    open_issues = gh_get(
        f'/repos/{REPO_OWNER}/{REPO_NAME}/issues',
        params={'state': 'open', 'per_page': 20}
    )
    return render_template('issues.html', issues=open_issues)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5555))
    app.run(host='0.0.0.0', port=port, debug=False)
