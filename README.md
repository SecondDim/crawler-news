# Python crawler for news

Use python scrapy build crawler for real-time Taiwan NEWS website.

使用 python scrapy 建置抓取台灣新聞網站即時新聞的爬蟲

## TODO LIST

- 整理 carssadra 權限，叢集變成 N=3
- 用成 k8s 部到 GKC，或是 VM 即可？
- 統一每隻爬蟲的 setting，分成 production & develop
- 實作多執行緒，同步爬蟲執行，使用 python script
- 可以考慮實作 docker install shell
- 持續修改 Bug
- 實作全網站一次性爬蟲（提供給 production）
- 消滅 TODO
- 寫一隻資料庫清理爬蟲

## TODO website

List from [Alexa台灣排名](https://www.prlass.com/2992/%E5%8F%B0%E7%81%A3%E7%B6%B2%E8%B7%AF%E6%96%B0%E8%81%9E%E5%AA%92%E9%AB%94%E6%B5%81%E9%87%8F%E6%8E%92%E5%90%8D-2018-01/)

1. [ettoday](https://www.ettoday.net/)
    - Can be optimized
1. [自由時報](https://www.ltn.com.tw/)
    - Can be optimized
1. [TVBS](https://news.tvbs.com.tw/)
    - Can be optimized
1. [三立新聞網](https://www.setn.com/)
    - Can be optimized
1. [FIX] [東森新聞](https://news.ebc.net.tw/)
    - Few special case articles no use p tag
    - Few special case articles video not in main span tag
1. [Test] [聯合新聞網](https://udn.com/news/index)
    - Can be optimized
1. [Pending] [頻果新聞網](https://tw.appledaily.com/home)
    - 要使用 javascript
    - 不能用 cookie,session
    - 新聞整體格式非主流，例：文章時間
1. [TODO] [風傳媒](https://www.storm.mg/)
1. [今日新聞](https://www.nownews.com/)
    - ajax.
    - Can be optimized
1. [TODO] [商業週刊](https://www.businessweekly.com.tw/)
    - Non-instant news
    - Mostly for business news
1. [中時電子報](https://www.chinatimes.com/)
    - Can be optimized
1. [TODO] [大紀元](https://www.epochtimes.com/)
    - Political position is too biased.
1. [中央通訊社](https://www.cna.com.tw/)
    - Can be optimized
1. [TODO] [關鍵評論網](https://www.thenewslens.com/)
    - Non-instant news
1. [TODO] [今周刊](https://www.businesstoday.com.tw/)
    - Maybe need javascript
    - Non-instant news
    - Mostly for business news

## Crawler step

1. Request real-time news lists.
2. Request news page from setp.1 list.
3. Parsing html and get target value. [item.py](crawler_news/items.py)
    - url
    - article_from
    - article_type
    - title
    - publish_date
    - authors
    - tags
    - text
    - text_html
    - images
    - video
    - links
4. Save into database. [pipelines.py](crawler_news/pipelines.py)
    - Default Use Cassandra
    - [TODO][feature] Use Mongo or Mysql
5. Done

## Requirement Install

### Develop Env

- python 3.7.6
- Cassandra 3.11.4
- Develop on macOS (main)

### python scrapy

```bash
    pip install scrapy
    # or
    pip3 install scrapy
```

### Install Cassandra Database

mac os

```bash
    brew install cassandra
```

python extension

```bash
    pip install cassandra-driver
    # or
    pip3 install cassandra-driver
```

start cassandra

```bash
    # start on bash
    cassandra -f

    # start on backgroud
```

### Install Mysql Database

mac os

```bash
    brew install mysql
```

python extension

```bash
    pip install PyMySQL
    # or
    pip3 install PyMySQL
```

## RUN Project

### Run all in localhost terminal

```bash
    ./run_spiders.sh
```

### Run in Docker use docker-compose.yml

1. build docker image

```bash
    docker build . -t crawler_news
```

If you want exec crawler without database. modify docker/setting.py and re-build.

```bash
    # run without database (linux base command)
    docker run --rm -it -v `pwd`/tmp:/src/tmp -v `pwd`/log:/src/log crawler_news
```

If you want exec single crawler. modify Dockerfile and re-build.

```Dockerfile
    CMD ["/bin/bash"]
    # or assign crawler
    CMD ["scrapy", "crawl", "ettoday"]
```

1. run docker-compose

```bash
    # start
    docker-compose up -d

    # stop
    docker-compose down
```
