# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl libertytimes

# TODO 檢查 parser

import scrapy

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
        'FEED_URI': 'tmp/%s-%s.json' % (name, str(int(time.time()))),
        'FEED_FORMAT': 'json',
    }

    def start_requests(self):
        list_url = '%s/list/breakingnews' % self.base_url
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        # * raise 404
        for page_url in response.css('ul.list>li>a.tit::attr(href)').getall():
            yield scrapy.Request(url=page_url, callback=self.parse_news)
            # raise "[******] 測試抓一筆就好"

    def parse_news(self, response):
        yield {
            'url': response.url,
            'title': self._parse_title(response),
            'publish_date': self._parse_publish_date(response),
            'authors': self._parse_authors(response),
            'tags': self._parse_tags(response),
            'text': self._parse_text(response),
            'text_html': self._parse_text_html(response),
            'images': self._parse_images(response),
            'video': self._parse_video(response),
            'links': self._parse_links(response),
        }

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
            return response.css('article *::text').re_first(r'記者.*報導')
        elif re.match('https://partners', response.url):
            return response.css('article span::text').re_first(r'[0-9-]+ [0-9:]+')
        else:
            return response.css('div.text>p *::text').re_first(r'記者.*報導')

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

