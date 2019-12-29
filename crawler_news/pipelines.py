# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from src.CassandraDatabase import CassandraDatabase

class CrawlerNewsPipeline(object):
    # TODO set database env in setting.py
    # def __init__(self, mongo_uri, mongo_db):
    #     self.mongo_uri = mongo_uri
    #     self.mongo_db = mongo_db

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get('MONGO_URI'),
    #         mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
    #     )

    def open_spider(self, spider):
        self.db = CassandraDatabase('test', 'test')
        self.db.create_table()

    def close_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        if item.get('url'):
            news = self.db.fetchOne(item['url'])
            if news == None:
                # TODO 塞進資料庫前，檢查資料格式

                try:
                    self.db.insert(dict(item))
                except Exception as e:
                    print("========== DB ERROR ==========")
                    print(e)
                    print(item)
                    print("------------------------------")
            else:
                # TODO version2 版本判斷
                pass

        else:
            raise DropItem("Missing item.url in %s" % item)

        return item
