# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ebc

import scrapy
from crawler_news.items import CrawlerNewsItem

import time
import re

class EBCSpider(scrapy.Spider):
    name = 'ebc'
    allowed_domains = ['news.ebc.net.tw']
    base_url = 'https://news.ebc.net.tw'

    date_str = str(time.strftime("%F", time.localtime()))

    custom_settings = {
        'LOG_FILE': 'log/%s-%s.log' % (name, date_str),
    }

    def start_requests(self):
        list_url = 'https://news.ebc.net.tw/Realtime'
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('div.white-box>a::attr(href)').getall():
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
        return response.css('div.fncnews-content>h1::text').get()

    def _parse_publish_date(self, response):
        pattern=r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2})' #2019/12/22 13:53
        string=response.css('div.info>span.small-gray-text::text').get()
        return re.search(pattern,string).group(0)

    def _parse_authors(self, response):
        pattern=r'(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2})' #2019/12/22 13:53
        string=response.css('div.info>span.small-gray-text::text').get()
        datetime=re.search(pattern,string).group(0)
        return [string.replace(datetime,'').strip()] #去掉日期時間

    def _parse_tags(self, response):
        return response.css('div.keyword>a::text').getall()

    def _parse_text(self, response):
        return response.css('span[data-reactroot=\'\'] p::text').getall()

    def _parse_text_html(self, response):
        return response.css('span[data-reactroot=\'\']').get()

    def _parse_images(self, response):
        allImgList=response.css('div.fncnews-content img::attr(src)').getall()
        imgURLs=[]
        for imgurl in allImgList:
            if re.match(r'https://img.news.ebc.net.tw\S+',imgurl):
                imgURLs.append(imgurl)
        return imgURLs

    def _parse_video(self, response):
        fb_video=response.css('span[data-reactroot=\'\']').css('iframe::attr(src)').getall()
        youtube=response.css('span[data-reactroot=\'\']').css('div.fb-video::attr(data-href)').getall()
        return fb_video+youtube

    def _parse_links(self, response):
        return response.css('span[data-reactroot=\'\']').css('a::attr(href)').getall()
