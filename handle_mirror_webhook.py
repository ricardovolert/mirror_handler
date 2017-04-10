import hglib
from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = False

REPO_PATH = './yt-hg'
BB_REPO = 'https://bitbucket.org/ngoldbaum/yt'
GH_REPO = 'git+ssh://git@github.com:ngoldbaum/yt-mirror.git'

@app.route('/',methods=['POST'])
def foo():
    try:
        repo = hglib.open(REPO_PATH)
        repo.close()
    except hglib.error.ServerError:
        hglib.clone(source=BB_REPO, dest=REPO_PATH)

    with hglib.open(REPO_PATH) as repo:
        repo.pull(BB_REPO)
        repo.push(GH_REPO)

    return "OK"
