import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class ChinatimesSpider(scrapy.Spider):
    name = 'chinatimes'
    allowed_domains = ['chinatimes.com']
    base_url = 'https://www.chinatimes.com'

    date_str = str(time.strftime("%F", time.localtime()))

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = '%s/realtimenews' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('section.article-list>ul>li h3.title>a::attr(href)').getall():
            page_url = self.base_url + page_url
            if not self.redis_client.exists(page_url):
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
        return response.css('article.article-box h1.article-title::text').get()

    def _parse_publish_date(self, response):
        return response.css('article.article-box time::attr(datetime)').get()

    def _parse_authors(self, response):
        authors = response.css('article.article-box div.author>a::text').getall()
        if len(authors) == 0:
            authors = [response.css('article.article-box div.author::text').get(default='').strip()]
        return authors

    def _parse_tags(self, response):
        return response.css('article.article-box div.article-hash-tag a::text').getall()

    def _parse_text(self, response):
        return response.css('article.article-box div.article-body p::text').getall()

    def _parse_text_html(self, response):
        return response.css('article.article-box div.article-body').get()

    def _parse_images(self, response):
        images_list = []
        images_list.extend(response.css('article.article-box div.main-figure').css('img::attr(src)').getall())
        images_list.extend(response.css('article.article-box div.article-body').css('img::attr(src)').getall())
        return images_list

    def _parse_video(self, response):
        return response.css('article.article-box div.article-body iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('article.article-box div.article-body').css('a::attr(href)').getall()
