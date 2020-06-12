FROM python:3.7-stretch

WORKDIR /src/

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir log && mkdir tmp

CMD ["/bin/bash", "run_spiders.sh"]

# -- DEBUG --
# docker build . -t crawler_news
# docker run --rm -it -v `pwd`/tmp:/src/tmp -v `pwd`/log:/src/log crawler_news
# docker run --rm -it -v `pwd`/tmp:/src/tmp -v `pwd`/log:/src/log --net crawler-news_default crawler_news:latest
# scrapy crawl ettoday
# CMD ["scrapy", "crawl", "ettoday"]
# CMD ["/bin/bash"]
# ENTRYPOINT [ "/bin/bash" ]
