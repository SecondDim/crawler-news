cd /home/ubuntu/crawler-news
git checkout . && git checkout $1 && git pull
mv .circleci/docker-compose.yml docker-compose.yml
sudo docker stop crawler_news && docker rm crawler_news
sudo docker-compose up -d --build
