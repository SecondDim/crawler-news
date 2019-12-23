# -*- coding: utf-8 -*-

# mac shell example
# scrapy crawl ebc -o tmp/ebc$(date +"%Y-%m-%d_%H_%M_%S").json

import scrapy

import re

class EBCSpider(scrapy.Spider):
    name = 'ebc'
    allowed_domains = ['news.ebc.net.tw']
    base_url = 'https://news.ebc.net.tw'
    # download_delay = 1

    def start_requests(self):
        list_url = 'https://news.ebc.net.tw/Realtime'
        yield scrapy.Request(url=list_url, callback=self.parse_list)

    def parse_list(self, response):
        for page_url in response.css('div.white-box>a::attr(href)').getall():
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
            'links': self._parse_links(response)
        }

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
        return string.replace(datetime,'').strip() #去掉日期時間

    def _parse_tags(self, response):
        return response.css('div.keyword>a::text').getall()

    def _parse_text(self, response):
        return response.css('span[data-reactroot=\'\'] p::text').getall()

    def _parse_text_html(self, response):
        return response.css('span[data-reactroot=\'\'] p').getall()

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
        