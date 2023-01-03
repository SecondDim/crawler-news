# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ettoday -a page=$(date +"%Y-%m-%d")

import scrapy
from crawler_news.items import CrawlerNewsItem
from scrapy.exceptions import IgnoreRequest

import time
import re

date_str = str(time.strftime("%F", time.localtime()))

class EtTodaySpider(scrapy.Spider):
    name = 'ettoday'
    allowed_domains = ['ettoday.net']
    base_url = 'https://www.ettoday.net'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),

        # https://speed.ettoday.net/robots.txt
        'ROBOTSTXT_OBEY': False
    }

    def start_requests(self):
        # TODO check date_page 1.exist 2.formet 3.default 2019-12-19
        date_page = getattr(self, 'page', time.strftime('%Y-%m-%d'))
        # * raise date_page.re('%Y-%m-%d')

        list_url = '%s/news/news-list.htm' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        # * raise 404
        for page_url in response.css('div.part_list_2>h3>a::attr(href)').getall():
            page_url = self.base_url+page_url
            if not self.redis_client.exists(page_url):
                yield scrapy.Request(url=page_url,callback=self.parse_news,cb_kwargs=dict(req_url=page_url))

    def parse_news(self, response, req_url):
        self.logger.info(f"request page: {req_url}")

        item = CrawlerNewsItem()

        item['url'] = req_url
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
        if re.match('https://fashion.', response.url):
            return response.css('h1.title_article::text').get()
        else:
            return response.css('h1.title::text').get()

    def _parse_publish_date(self, response):
        if re.match('https://pets.', response.url):
            return response.css('time.news-time::text').get(default='').strip()
        if re.match('https://pets.', response.url):
            return response.css('.subject_article h1::text').get(default='').strip()
        else:
            return response.css('time.date::text').get(default='').strip()

    def _parse_authors(self, response):
        authors = response.css('div.story>p *::text')
        if authors.re_first(r'(^[^▲▼（\s]*／[^）\s]*)') != None:
            return [authors.re_first(r'(^[^▲▼（\s]*／[^）\s]*)')]
        elif authors.re_first(r'(^.+\/.+)') != None:
            return [authors.re_first(r'(^.+\/.+)')]

    def _parse_tags(self, response):
        news_tags = []
        if re.match('https://www.', response.url):
            news_tags = news_tags + response.css('div.part_menu_5>a::text').getall()
            news_tags = news_tags + response.css('div.part_tag_1>a::text').getall()
        elif re.match('https://star.', response.url):
            news_tags = response.css('div.menu_txt_2>a::text').getall()
        elif re.match('https://fashion.', response.url):
            news_tags = response.css('div.part_keyword>a::text').getall()
        elif re.match('https://pets.', response.url) \
                or re.match('https://sports.', response.url)\
                or re.match('https://house.', response.url)\
                or re.match('https://travel.', response.url)\
                or re.match('https://health.', response.url)\
                or re.match('https://speed.', response.url)\
                or re.match('https://discovery.', response.url):
            news_tags = response.css('div.tag>a::text').getall()
        elif re.match('https://forum.', response.url):
            news_tags = response.css('div.part_tag>a::text').getall()
        else:
            pass

        return news_tags

    def _parse_text(self, response):
        return response.css('div.story>p *::text').getall()

    def _parse_text_html(self, response):
        return response.css('div.story').get()

    def _parse_images(self, response):
        return response.css('div.story').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('div.story iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('div.story').css('a::attr(href)').getall()
