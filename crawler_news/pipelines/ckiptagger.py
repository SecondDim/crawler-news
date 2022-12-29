# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json

daily_sec = 60 * 60 * 24

class CkiptaggerPipeline:
    def _json_dumps_item(self, item, key):
        if item.get(key):
            return json.dumps(item.get(key), ensure_ascii=False)
        else:
            return None

    def process_item(self, item, spider):
        spider.logger.info('send to work queue for parse. %s' % item.get('url'))

        spider.redis_client.lpush('ckiptagger_worker_queue', json.dumps( {
            'url': item.get('url'),
            'text': item.get('text')
        }, ensure_ascii=False ))

        # TODO 之後移到專屬pipeline才對
        self.redis_client.set(item.get('url'), json.dumps( dict(item) ), ex=daily_sec)

        return item
