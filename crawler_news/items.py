# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerNewsItem(scrapy.Item):
    url = scrapy.Field() # str
    title = scrapy.Field() # str
    publish_date = scrapy.Field() # str
    authors = scrapy.Field() # list
    tags = scrapy.Field() # list
    text = scrapy.Field() # list
    text_html = scrapy.Field() # str
    images = scrapy.Field() # list
    video = scrapy.Field() # list
    links = scrapy.Field() # list
