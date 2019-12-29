# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl tvbs

# TODO 檢查 parser

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class TVBSSpider(scrapy.Spider):
    name = 'tvbs'
    allowed_domains = ['tvbs.com.tw']
    base_url = 'https://news.tvbs.com.tw'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        yield scrapy.Request(url=self.base_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('div#now_news>ul>li>a::attr(href)').getall():
            yield scrapy.Request(url=self.base_url + page_url, callback=self.parse_news)

    def parse_news(self, response):
        item = CrawlerNewsItem()

        item['url'] = response.url
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
        return response.css('h1::text').get()

    def _parse_publish_date(self, response):
        return response.css('div.time::text').get()

    def _parse_authors(self, response):
        return list(map(lambda x: x.strip(), response.css('h4 *::text').getall()))

    def _parse_tags(self, response):
        return response.css('div.adWords>ul>li a::text').getall()

    def _parse_text(self, response):
        return response.css('div.newsdetail_content div.contxt *::text').getall()

    def _parse_text_html(self, response):
        return response.css('div.newsdetail_content div.contxt').get()

    def _parse_images(self, response):
        return response.css('div.newsdetail_content div.contxt').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('div.newsdetail_content div.contxt #ytframe iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('div.newsdetail_content div.contxt').css('a::attr(href)').getall()
