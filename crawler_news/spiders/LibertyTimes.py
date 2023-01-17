import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

date_str = str(time.strftime("%F", time.localtime()))

class LibertyTimesSpider(scrapy.Spider):
    name = 'libertytimes'
    allowed_domains = ['ltn.com.tw']
    base_url = 'https://news.ltn.com.tw'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = '%s/list/breakingnews' % self.base_url
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        page_url_list = response.css('ul.list>li>a.tit::attr(href)').getall()

        self.logger.info(page_url_list)

        for page_url in page_url_list:
            if not self.redis_client.exists(page_url):
                yield scrapy.Request(url=page_url, callback=self.parse_news)

    def parse_news(self, response):
        req_url = response.request.url

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
        return response.css('h1::text').get()

    def _parse_publish_date(self, response):
        publish_date = response.css('div.content *::text').re_first(r'[0-9/-]+[\s]+[0-9:]+', default='').strip()

        if re.match('https://news', response.url):
            publish_date = response.css('div.whitecon span.time::text').get(default='').strip()
        elif re.match('https://sports', response.url):
            publish_date = response.css('div.c_time::text').get(default='').strip()
        elif re.match('https://istyle', response.url):
            publish_date = response.css('div.label-date::text').get(default='').strip()
        elif re.match('https://ent', response.url):
            publish_date = response.css('div.content div.date::text').get(default='').strip()
        elif re.match('https://auto', response.url):
            publish_date = response.css('div.con_writer span.h1dt::text').get(default='').strip()

        return publish_date

    def _parse_authors(self, response):
        return [response.css('div.content *::text').re_first(r'[\[〔［].+[／].+[］〕\]]',default='')]

    def _parse_tags(self, response):
        # no tags
        return []

    def _parse_text(self, response):
        text = []
        reStr = ''
        if re.match('https://sports', response.url):
            reStr = 'div[itemprop="articleBody"] p::text'
        elif re.match('https://ent', response.url):
            reStr = 'div.news_content p:not([class]) *::text'
        else:
            reStr = 'div.text>p:not([class]) *::text'

        if re.match('https://health', response.url) or re.match('https://art', response.url):
            _text = []
            for v in response.css(reStr).getall():
                if v.strip().startswith('☆') or v.strip().startswith('自由健康網') or v.strip().startswith('自由藝文網'):
                    continue
                _text.append(v.strip())
        else:
            _text = response.css(reStr).getall()

        for t in _text:
            if t.strip() != '':
                text.append(t.strip())

        return text

    def _parse_text_html(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').get()
        elif re.match('https://ent', response.url):
            return response.css('div.news_content').get()
        else:
            return response.css('div.text').get()

    def _parse_images(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').css('img::attr(src)').getall()
        elif re.match('https://ent', response.url):
            return response.css('div.news_content').css('img::attr(data-original)').getall()
        else:
            return response.css('div.text').css('img::attr(src)').getall()


    def _parse_video(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').css('iframe::attr(src)').getall()
        elif re.match('https://ent', response.url):
            return response.css('div.news_content').css('iframe::attr(src)').getall()
        else:
            return response.css('div.text').css('iframe::attr(src)').getall()

    def _parse_links(self, response):
        if re.match('https://sports', response.url):
            return response.css('div.news_p').css('a::attr(href)').getall()
        elif re.match('https://ent', response.url):
            return response.css('div.news_content').css('a::attr(href)').getall()
        else:
            return response.css('div.text').css('a::attr(href)').getall()

