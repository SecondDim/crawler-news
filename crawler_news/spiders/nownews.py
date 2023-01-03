import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re
import json

date_str = str(time.strftime("%F", time.localtime()))

class NownewsSpider(scrapy.Spider):
    name = 'nownews'
    allowed_domains = ['nownews.com']
    base_url = 'https://www.nownews.com'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
        # 'LOG_FILE': None,
        # 'DEFAULT_REQUEST_HEADERS': {
        #     'Accept': '*/*',
        #     'Referer': 'https://www.nownews.com/',
        # }
    }

    def start_requests(self):
        list_url = '%s/cat/breaking/' % (self.base_url)
        print(list_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        page_url_list = response.css('a::attr(href)').getall()
        for page_url in page_url_list:

            if re.match('https://www.nownews.com/news/*', page_url) and not self.redis_client.exists(page_url):
                yield scrapy.Request(url=page_url, callback=self.parse_news)

    def parse_news(self, response):
        req_url = response.request.url

        self.logger.info(f"request page: {req_url}")

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
        return response.css('h1.article-title::text').get()

    def _parse_publish_date(self, response):
        return response.css('time span::text').get()

    def _parse_authors(self, response):
        return [response.css('div.infoBlk>div>p::text').get()]

    def _parse_tags(self, response):
        return response.css('div.keywordBlk ul.tag li>a::text').getall()

    def _parse_text(self, response):
        text = []
        for t in response.css('article[itemprop=articleBody]::text').getall():
            if t.strip() != '':
                text.append(t.strip())
        return text

    def _parse_text_html(self, response):
        return response.css('article[itemprop=articleBody]').get()

    def _parse_images(self, response):
        return response.css('div.containerBlk').css('img::attr(src)').getall()

    def _parse_video(self, response):
        # TODO
        return response.css('article noscript>iframe::attr(src)').getall()

    def _parse_links(self, response):
        # TODO
        # links = response.css('article div.td-post-content').css('a::attr(href)').getall()
        # return list(filter(lambda x:x if not x == '#' else None , links))
        return []
