# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Item

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import json

daily_sec = 60 * 60 * 24

class CrawlerNewsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # print('[middleware] CrawlerNewsSpiderMiddleware from_crawler')

        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # print('[middleware] CrawlerNewsSpiderMiddleware process_spider_input')

        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # print('[middleware] CrawlerNewsSpiderMiddleware process_spider_output')

        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            if is_item(i) :
                spider.redis_client.set(i.get('url'), json.dumps( dict(i) ), ex=daily_sec)
            yield i

    def process_spider_exception(self, response, exception, spider):
        # print('[middleware] CrawlerNewsSpiderMiddleware process_spider_exception')

        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # print('[middleware] CrawlerNewsSpiderMiddleware process_start_requests')

        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        # print('[middleware] CrawlerNewsSpiderMiddleware spider_opened')

        spider.logger.info('Spider opened: %s' % spider.name)


class CrawlerNewsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # print('[middleware] CrawlerNewsDownloaderMiddleware from_crawler')

        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # print('[middleware] CrawlerNewsDownloaderMiddleware process_request')

        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # print('[middleware] CrawlerNewsDownloaderMiddleware process_response')

        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # print('[middleware] CrawlerNewsDownloaderMiddleware process_exception')

        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        # print('[middleware] CrawlerNewsDownloaderMiddleware spider_opened')

        spider.logger.info('Spider opened: %s' % spider.name)
