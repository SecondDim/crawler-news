# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl tvbs

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

from lxml import etree
from scrapy import Selector

class CnaSpider(scrapy.Spider):
    name = 'cna'
    allowed_domains = ['cna.com.tw']
    base_url = 'https://www.cna.com.tw'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        list_url = '%s/list/aall.aspx' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('ul#myMainList>li>a::attr(href)').getall():
            yield scrapy.Request(url=page_url, callback=self.parse_news)

    def parse_news(self, response):
        item = CrawlerNewsItem()

        item['url'] = response.url
        item['article_from'] = self.name
        item['article_type'] = 'news'

        item['title'] = self._parse_title(response)
        item['publish_date'] = self._parse_publish_date(response)
        item['authors'] = self._parse_authors(response)
        item['tags'] = self._parse_tags(response)
        item['text'] = self._parse_text(response)
        item['text_html'] = self._parse_text_html(response)
        item['images'] = self._parse_images(response)
        item['video'] = self._parse_video(response)
        item['links'] = self._parse_links(response)

        return item

    def _parse_title(self, response):
        return response.css('article.article h1::text').get()

    def _parse_publish_date(self, response):
        return response.css('article.article div.timeBox span::text').get()

    def _parse_authors(self, response):
        # inconsistent format
        pre_authors = response.css('article.article div.paragraph p::text').re(r'^（[^）]*）|（[^）]*）[0-9]*$')
        return list(map(lambda x: x[1:].split('）')[0], pre_authors))

    def _parse_tags(self, response):
        # no tag
        return []

    def _parse_text(self, response):
        return response.css('article.article div.paragraph p::text').getall()

    def _parse_text_html(self, response):
        return response.css('article.article div.paragraph').get()

    def _parse_images(self, response):
        # parser error with div.fullPic
        return response.css('article.article').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('article.article div.media iframe::attr(data-src)').getall()

    def _parse_links(self, response):
        return response.css('article.article div.paragraph p').css('a::attr(href)').getall()
