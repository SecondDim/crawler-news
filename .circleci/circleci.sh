cd /home/ubuntu/crawler-news
git reset HEAD^ && git checkout $1 && git pull
sudo docker stop crawler_news && docker rm crawler_news
sudo docker-compose -f .circleci/docker-compose.yml up -d --build
