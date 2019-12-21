# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl setn -o tmp/setn.json
# scrapy crawl setn -o tmp/setn_$(date +"%Y-%m-%d_%H:%M:%S").json

# TODO 檢查 parser

import scrapy

import re

class LibertyTimesSpider(scrapy.Spider):
    name = 'setn'
    allowed_domains = ['setn.com']
    base_url = 'https://www.setn.com'
    # download_delay = 1

    def start_requests(self):
        list_url = 'https://www.setn.com/ViewAll.aspx?PageGroupID=1'
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('h3.view-li-title>a.gt ::attr(href)').getall():
            yield scrapy.Request(url=self.base_url+page_url, callback=self.parse_news)

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
        # TODO 娛樂版
        return response.css('h1.news-title-3::text').get()

    def _parse_publish_date(self, response):
        # TODO 娛樂版
        return response.css('time.page-date::text').get()

    def _parse_authors(self, response):
        # TODO 娛樂版
        return response.css('div#Content1>p::text').get()

    def _parse_tags(self, response):
        return response.css('div.page-keyword-area ul>li>a>strong::text').getall()

    def _parse_text(self, response):
        return response.css('article p *::text').getall()

    def _parse_text_html(self, response):
        return response.css('article').getall()

    def _parse_images(self, response):
        return response.css('article').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('article').css('iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('article').css('a::attr(href)').getall()
        