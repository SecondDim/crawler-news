# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.exceptions import DropItem
from src.MysqlDatabase import MysqlDatabase

class MysqlPipeline(object):

    def open_spider(self, spider):
        settings = spider.settings
        self.db = MysqlDatabase(host=settings['MYSQL_HOST'],
                             port=settings['MYSQL_PORT'],
                             user=settings['MYSQL_USER'],
                             password=settings['MYSQL_PASSWORD'],
                             db=settings['MYSQL_DB'],
                             table=settings['MYSQL_TABLE'],
                             charset=settings['MYSQL_CHARSET'])

    def close_spider(self, spider):
        self.db.close()

    def _json_dumps_item(self, item, key):
        if item.get(key):
            return json.dumps(item.get(key), ensure_ascii=False)
        else:
            return None

    async def process_item(self, item, spider):
        if not item.get('url'):
            raise DropItem("Missing item.url in %s" % item)

        if not self.db.news_exist(item['url']):
            # TODO 塞進資料庫前，檢查資料格式

            item['authors'] = self._json_dumps_item(item, 'authors')
            item['tags'] = self._json_dumps_item(item, 'tags')
            item['text'] = self._json_dumps_item(item, 'text')
            item['images'] = self._json_dumps_item(item, 'images')
            item['video'] = self._json_dumps_item(item, 'video')
            item['links'] = self._json_dumps_item(item, 'links')

            try:
                self.db.insert(dict(item))
            except Exception as e:
                spider.logger.error("---------- DB INSERT ERROR ----------")
                spider.logger.error(e)
                spider.logger.error(item)
                spider.logger.error("==============================")
        else:
            # TODO version2 版本判斷
            pass

        return item
