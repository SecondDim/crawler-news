# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

import redis

class RedisClient():
    @classmethod
    def from_crawler(cls, crawler):
        # first check if the extension should be enabled and raise
        # NotConfigured otherwise
        # if not crawler.settings.getbool('MYEXT_ENABLED'):
        #     raise NotConfigured

        # get the number of items from settings
        # item_count = crawler.settings.getint('MYEXT_ITEMCOUNT', 1000)

        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        # crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        # crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        host = spider.settings.get('REDIS_HOST', 'localhost')
        port = spider.settings.get('REDIS_PORT', 6379)
        db = spider.settings.get('REDIS_DATABASE', 0)

        spider.logger.info(f"Connect redis host:{host}, port:{port}, db:{db}")

        spider.redis_client = redis.Redis(host, port, db)
