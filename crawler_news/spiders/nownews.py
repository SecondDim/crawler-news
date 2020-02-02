# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ettoday -a page=$(date +"%Y-%m-%d")

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re
import json

class NownewsSpider(scrapy.Spider):
    name = 'nownews'
    allowed_domains = ['nownews.com']
    base_url = 'https://www.nownews.com'

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'LOG_FILE': 'log/%s-%s.log' % (name, str(int(time.time()))),
        'LOG_LEVEL': 'DEBUG',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': '*/*',
            'Referer': 'https://www.nownews.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }
    }

    def start_requests(self):
        list_url = '%s/WirelessFidelity/staticFiles/nownewsIndexpage/indexpageCacheJson' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        # * raise 404
        # * raise json decode error
        json_body = json.loads(response.body_as_unicode())
        for row in json_body:
            yield scrapy.Request(url=row['link'], callback=self.parse_news)

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
        return response.css('header>h1::text').get()

    def _parse_publish_date(self, response):
        return response.css('header>div.td-module-meta-info>span>time::text').get()

    def _parse_authors(self, response):
        return [response.css('header>div.td-module-meta-info>div.td-post-author-name::text').get().strip()]

    def _parse_tags(self, response):
        return response.css('footer>div.td-post-source-tags>ul>li>a::text').getall()

    def _parse_text(self, response):
        return response.css('article div.td-post-content span[itemprop=articleBody] p *::text').getall()

    def _parse_text_html(self, response):
        return response.css('article div.td-post-content').get()

    def _parse_images(self, response):
        return response.css('article div.td-post-content').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('article noscript>iframe::attr(src)').getall()

    def _parse_links(self, response):
        links = response.css('article div.td-post-content').css('a::attr(href)').getall()
        return list(filter(lambda x:x if not x == '#' else None , links))
