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
BB_REPO_PATH='./yt-hg' BB_REPO='https://bitbucket.org/yt_analysis/yt' \
GH_REPO_PATH='./yt-git' GH_REPO=git+ssh://git@github.com/yt-project/yt ./run.sh
```

Alternatively you can edit `handle_mirror_webhook.py` to use custom
hard-coded paths.

Finally you will need to set up a new push webhook on the bitbucket
repository. See [this
page](https://confluence.atlassian.com/bitbucket/manage-webhooks-735643732.html)
for more information.

## Docker

```
export TOKEN=...  # Personal token with 'repo' scope

docker run \
  --rm -ti \
  -e BB_REPO_PATH=/tmp/yt-hg \
  -e GH_REPO_PATH=/tmp/yt-git \
  -e BB_REPO=https://bitbucket.org/yt_analysis/yt \
  -e GH_REPO=https://${TOKEN}@github.com/xarthisius/yt.git \
  -v $PWD:/app \
  -p 5000:5000 \
  jfloff/alpine-python:2.7-slim \
    -a git \
    -a mercurial \
    -r /app/requirements.txt \
      -- python /app/handle_mirror_webhook.py
```
