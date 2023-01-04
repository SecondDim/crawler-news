import scrapy
from crawler_news.items import CrawlerNewsItem

import time

date_str = str(time.strftime("%F", time.localtime()))

class TVBSSpider(scrapy.Spider):
    name = 'tvbs'
    allowed_domains = ['tvbs.com.tw']
    base_url = 'https://news.tvbs.com.tw'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = '%s/realtime' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('div.news_list>div.list>ul>li>a:first-child::attr(href)').getall():
            page_url = self.base_url + page_url
            if not self.redis_client.exists(page_url):
                yield scrapy.Request(url=page_url, callback=self.parse_news,cb_kwargs=dict(req_url=page_url))

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
        return response.css('h1.title::text').get()

    def _parse_publish_date(self, response):
        return response.css('div.author::text').re_first(r'[0-9]+/[0-9]+/[0-9]+ [0-9]+:[0-9]+')

    def _parse_authors(self, response):
        return response.css('div.author>a::text').getall()

    def _parse_tags(self, response):
        tags = []
        for t in response.css('div.article_keyword>a::text').getall():
            tags.append(t.lstrip('#'))
        return tags

    def _parse_text(self, response):
        text = []
        for t in response.css('#news_detail_div::text,#news_detail_div>p::text').getall():
            if t.strip() != '':
                text.append(t.strip())
        return text

    def _parse_text_html(self, response):
        return response.css('#news_detail_div').get()

    def _parse_images(self, response):
        return response.css('.article_new').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('.article_new #ytframe iframe::attr(src)').getall()

    def _parse_links(self, response):
        return response.css('.article_new').css('a::attr(href)').getall()
