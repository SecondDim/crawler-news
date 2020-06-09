# /bin/bash

set -xe

cd /home/ubuntu/crawler-news
git checkout . && git checkout $1 && git pull
cp .circleci/docker-compose.yml docker-compose.yml
cp /home/ubuntu/config/settings.py crawler_news/
sudo docker stop crawler_news && sudo docker rm crawler_news
sudo docker-compose up -d --build
