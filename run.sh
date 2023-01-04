#! /bin/bash

# crontab -e
# */5 * * * * /home/bentsou/Project/crawler-news/run.sh

# set -x

workdir=/home/bentsou/Project/crawler-news/
cd $workdir

. $HOME/.profile;
/usr/bin/python $workdir/app.py

# set +x
