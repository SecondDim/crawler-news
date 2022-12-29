# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CrawlerNewsItem(scrapy.Item):
    url = scrapy.Field() # str
    article_from = scrapy.Field() # str
    article_type = scrapy.Field() # str
    title = scrapy.Field() # str
    publish_date = scrapy.Field() # str
    authors = scrapy.Field() # list json
    tags = scrapy.Field() # list json
    text = scrapy.Field() # list json
    text_html = scrapy.Field() # str
    images = scrapy.Field() # list json
    video = scrapy.Field() # list json
    links = scrapy.Field() # list json
