# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl setn

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class SetnSpider(scrapy.Spider):
    name = 'setn'
    allowed_domains = ['setn.com']
    base_url = 'https://www.setn.com'

    date_str = str(time.strftime("%F", time.localtime()))

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = 'https://www.setn.com/ViewAll.aspx?PageGroupID=1'
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('h3.view-li-title>a.gt ::attr(href)').getall():
            yield scrapy.Request(url=self.base_url+page_url, callback=self.parse_news)

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
        if re.match('https://www.setn.com/e', response.url):
            return response.css('h1#newsTitle::text').get()
        else:
            return response.css('h1.news-title-3::text').get()

    def _parse_publish_date(self, response):
        if re.match('https://www.setn.com/e', response.url):
            return response.css('div.titleBtnBlock>div.time::text').get()
        else:
            return response.css('time.page-date::text').get()

    def _parse_authors(self, response):
        if re.match('https://www.setn.com/e', response.url):
            return [response.css('div.Content2>p::text').get()]
        else:
            return [response.css('div#Content1>p::text').get()]

    def _parse_tags(self, response):
        return response.css('div.page-keyword-area ul>li>a>strong::text').getall()

    def _parse_text(self, response):
        return response.css('article p *::text').getall()

    def _parse_text_html(self, response):
        return response.css('article').get()

    def _parse_images(self, response):
        return response.css('article').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('article').css('iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('article').css('a::attr(href)').getall()
