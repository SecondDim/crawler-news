# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ettoday -a page=$(date +"%Y-%m-%d")

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class AppleDailySpider(scrapy.Spider):
    name = 'appledaily'
    allowed_domains = ['tw.appledaily.com']
    base_url = 'https://tw.appledaily.com'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        list_url = '%s/new/realtime' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        # * raise 404
        for page_url in response.css('div.abdominis>ul.rtddd>li a::attr(href)').getall():
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
        return response.css('header>div>h2>span::text').get()

    # -------------------- 以下未完成 --------------------
    def _parse_publish_date(self, response):
        return response.css('div#story_bady_info span::text').get()

    def _parse_authors(self, response):
        authors = response.css('div#story_bady_info>div>a::text').getall()
        if len(authors) == 0:
            authors = response.css('div#story_bady_info>div::text').getall()
        return authors

    def _parse_tags(self, response):
        return response.css('div#story_tags>a::text').getall()

    def _parse_text(self, response):
        return response.css('div#article_body p *::text').getall()

    def _parse_text_html(self, response):
        return response.css('div#article_body').get()

    def _parse_images(self, response):
        return response.css('div#article_body').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('div.video-container>iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('div#article_body').css('a::attr(href)').getall()

