import hglib
import os
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = False

def get_environment_variable(variable, default):
    try:
        return os.environ[variable]
    except KeyError:
        return default

REPO_PATH = get_environment_variable('REPO_PATH', './yt-hg')
BB_REPO = get_environment_variable('BB_REPO', 'https://bitbucket.org/ngoldbaum/yt')
GH_REPO = get_environment_variable(
    'GH_REPO', 'git+ssh://git@github.com:ngoldbaum/yt-mirror.git')

@app.route('/', methods=['POST'])
def foo():
    configs = ['extensions.hgext.bookmarks=', 'extensions.hggit=']
    try:
        repo = hglib.open(REPO_PATH, configs=configs)
        repo.close()
    except hglib.error.ServerError:
        hglib.clone(source=BB_REPO, dest=REPO_PATH)

    with hglib.open(REPO_PATH, configs=configs) as repo:
        repo.pull(BB_REPO)
        repo.push(GH_REPO)

    return "OK"
