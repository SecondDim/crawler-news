# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ettoday -a page=$(date +"%Y-%m-%d")

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class LocalhostSpider(scrapy.Spider):
    name = 'localhost'
    allowed_domains = ['localhost']
    base_url = 'http://localhost'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse)

    def parse(self, response):
        print("[*] OK!")
