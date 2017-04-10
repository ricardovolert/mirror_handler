# yt Repository Mirror Handler

This is a simple flask web service for mirroring git bitbucket yt
repository to github.

## Installation

You will need to first install python, mercurial, and hg-git. In
addition the mercurial installation will need to be configured to use
the [hg-git extension](http://hg-git.github.io/).

Finally set up a virtualenv for this service using the accompanying
`requirements.txt` file.

## Configuration

Set the `REPO_PATH`, `BB_REPO`, and `GH_REPO` environment variables
and execute run.sh: 

```
REPO_PATH='./yt-hg' BB_REPO='https://bitbucket.org/yt_analysis/yt' GH_REPO=git+ssh://git@github.com/yt-project/yt ./run.sh
```

Alternatively you can edit `handle_mirror_webhook.py` to use custom
hard-coded paths.

## Docker

TODO: pass ssh credentials

```
docker run \
  --rm -ti \
  -e FLASK_APP=/app/handle_mirror_webhook.py \
  -v $PWD:/app \
  -p 5000:5000 \
  jfloff/alpine-python:2.7-slim \
    -a git \
    -a mercurial \
    -r /app/requirements.txt \
      -- flask run --host=0.0.0.0
```
