#! /bin/bash

# crontab -e
# */5 * * * * /home/bentsou/Project/crawler-news/run.sh

# set -x

workdir=$(dirname "$0")
cd "$workdir"

# . $HOME/.profile;
python app.py

# set +x
