# Python crawler for news

Use python build crawler for Taiwan NEWS website.

## TODO

List from [Alexa台灣排名](https://www.prlass.com/2992/%E5%8F%B0%E7%81%A3%E7%B6%B2%E8%B7%AF%E6%96%B0%E8%81%9E%E5%AA%92%E9%AB%94%E6%B5%81%E9%87%8F%E6%8E%92%E5%90%8D-2018-01/)

1. [Test] [ettoday](https://www.ettoday.net/)
    - videos
    - data uncheck
1. [Test] [自由時報](https://www.ltn.com.tw/)
    - videos
    - data uncheck
1. [Test] [TVBS](https://news.tvbs.com.tw/)
    - data uncheck
1. [Test] [三立新聞網](https://www.setn.com/)
    - data uncheck
1. [Test] [東森新聞](https://news.ebc.net.tw/)
    - data uncheck
1. [Test] [聯合新聞網](https://udn.com/news/index)
    - data uncheck
1. [Pending] [頻果新聞網](https://tw.appledaily.com/home)
    - 要使用 javascript
    - 不能用 cookie,session
    - 新聞整體格式非主流，例：文章時間
1. [風傳媒](https://www.storm.mg/)
1. [Test] [今日新聞](https://www.nownews.com/)
    - Need javascript, ddos protection.
    - Is immediate news?
1. [商業週刊](https://www.businessweekly.com.tw/)
    - Non-instant news
    - Mostly for business news
1. [中時電子報](https://www.chinatimes.com/)
1. [大紀元](https://www.epochtimes.com/)
    - Political position is too biased.Need filiter sth artical.
1. [中央通訊社](https://www.cna.com.tw/)
1. [關鍵評論網](https://www.thenewslens.com/)
    - Non-instant news
1. [今周刊](https://www.businesstoday.com.tw/)
    - Maybe need javascript
    - Non-instant news
    - Mostly for business news

## Crawler step

1. Request news lists and get page url to add to queue.
    - Use database queue.
    - Because Crawler speed is too slow, no need memery queue.
2. Request news page.
3. Parsing html and get target value.
    - News url
    - Original html
    - News title
    - News text
    - News tag
    - News datetime
4. Save into database
    - Use sqlite3
    - Maybe use Mysql in future
5. Done

## Install scrapy

```bash
    pip install scrapy
    or
    pip3 install scrapy
```

## Install Cassandra Database

mac os

```bash
    brew install cassandra
```

python extension

```bash
    pip install cassandra-driver
    or
    pip3 install cassandra-driver
```

start cassandra

```bash
    # start on bash
    cassandra -f
```
