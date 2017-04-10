import git
import hglib
import logging
import os
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

GH_REPO_PATH = os.environ.get('GH_REPO_PATH', '/tmp/yt-git')
BB_REPO_PATH = os.environ.get('BB_REPO_PATH', '/tmp/yt-hg')
BB_REPO = os.environ.get('BB_REPO', 'https://bitbucket.org/ngoldbaum/yt')
GH_REPO = os.environ.get(
    'GH_REPO', 'git+ssh://git@github.com:ngoldbaum/yt-mirror.git')


@gen.coroutine
def sync_repos():
    configs = ['extensions.hggit=']
    try:
        repo = hglib.open(BB_REPO_PATH, configs=configs)
        repo.close()
    except hglib.error.ServerError:
        hglib.clone(source=BB_REPO, dest=BB_REPO_PATH)

    try:
        gh_repo = git.Repo(GH_REPO_PATH)
        origin = gh_repo.remote('origin')
        origin.pull('master')
        gh_repo.close()
    except git.exc.NoSuchPathError:
        gh_repo = git.Repo.init(GH_REPO_PATH)
        origin = gh_repo.create_remote('origin', GH_REPO)
        origin.pull('master')
        gh_repo.close()

    with hglib.open(BB_REPO_PATH, configs=configs) as repo:
        repo.pull(BB_REPO)
        repo.push(GH_REPO_PATH)

    with git.Repo(GH_REPO_PATH) as repo:
        origin = repo.remote('origin')
        origin.push('master')


class MainHandler(RequestHandler):

    @gen.coroutine
    def post(self):
        IOLoop.current().spawn_callback(sync_repos)
        self.set_status(202)
        self.finish()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    handlers = [
        (r"/", MainHandler),
    ]

    app = Application(handlers)
    app.listen(5000)
    IOLoop.current().start()
