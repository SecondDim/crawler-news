import scrapy
from crawler_news.items import CrawlerNewsItem

import time

date_str = str(time.strftime("%F", time.localtime()))

class CnaSpider(scrapy.Spider):
    name = 'cna'
    allowed_domains = ['cna.com.tw']
    base_url = 'https://www.cna.com.tw'

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = '%s/list/aall.aspx' % (self.base_url)
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('#jsMainList>li>a::attr(href)').getall():
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
        return response.css('article.article h1 *::text').get()

    def _parse_publish_date(self, response):
        return response.css('article.article div.timeBox span::text').get()

    def _parse_authors(self, response):
        # inconsistent format
        pre_authors = response.css('article.article div.paragraph p::text').re(r'^（[^）]*）|（[^）]*）[0-9]*$')
        return list(map(lambda x: x[1:].split('）')[0], pre_authors))

    def _parse_tags(self, response):
        tags = []
        for t in response.css('.keywordTag a::text').getall():
            tags.append(t.lstrip('#'))
        return tags

    def _parse_text(self, response):
        ret = []
        for i in range(0,10):
            if len(response.css('article.article div.paragraph:nth-of-type(%s) p::text' % i).getall()) != 0:
                ret = response.css('article.article div.paragraph:nth-of-type(%s) p::text' % i).getall()
                break
        return ret

    def _parse_text_html(self, response):
        return response.css('article.article div.paragraph').get()

    def _parse_images(self, response):
        # parser error with div.fullPic
        return response.css('article.article').css('img::attr(src)').getall()

    def _parse_video(self, response):
        return response.css('article.article div.media iframe::attr(data-src)').getall()

    def _parse_links(self, response):
        return response.css('article.article div.paragraph p').css('a::attr(href)').getall()
