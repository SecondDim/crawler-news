# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl libertytimes

# TODO 檢查 parser

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class LibertyTimesSpider(scrapy.Spider):
    name = 'libertytimes'
    allowed_domains = ['ltn.com.tw']
    base_url = 'https://news.ltn.com.tw'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        list_url = '%s/list/breakingnews' % self.base_url
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        # * raise 404
        for page_url in response.css('ul.list>li>a.tit::attr(href)').getall():
            yield scrapy.Request(url=page_url, callback=self.parse_news)

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
        if re.match('https://sports', response.url):
            return response.css('div.c_time::text').get()
        elif re.match('https://partners', response.url):
            return response.css('article span::text').re_first(r'[0-9-]+ [0-9:]+')
        elif response.css('div.text>span.time::text').get() != None:
            return response.css('div.text>span.time::text').get().strip()
        else:
            return ''

    def _parse_authors(self, response):
        if re.match('https://sports', response.url):
            return [response.css('article *::text').re_first(r'記者.*報導',defult='')]
        elif re.match('https://partners', response.url):
            return [response.css('article span::text').re_first(r'[0-9-]+ [0-9:]+',defult='')]
        else:
            return [response.css('div.text>p *::text').re_first(r'記者.*報導',defult='')]

    def _parse_tags(self, response):
        # no tags
        return []

    def _parse_text(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p p *::text').getall()
        else:
            return response.css('div.text>p *::text').getall()

    def _parse_text_html(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p *').get()
        else:
            return response.css('div.text').get()

    def _parse_images(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').css('img::attr(src)').getall()
        else:
            return response.css('div.text').css('img::attr(src)').getall()


    def _parse_video(self, response):
        # TODO
        return []

    def _parse_links(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').css('a::attr(href)').getall()
        else:
            return response.css('div.text').css('a::attr(href)').getall()

