# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import json
import time

daily_sec = 60 * 60 * 24
time_epoch_unit = 5 * 60

class CkiptaggerPipeline:
    def _json_dumps_item(self, item, key):
        if item.get(key):
            return json.dumps(item.get(key), ensure_ascii=False)
        else:
            return None

    def process_item(self, item, spider):
        spider.logger.info('send to work queue for parse. %s' % item.get('url'))

        time_epoch = int((time.time() - time_epoch_unit) / time_epoch_unit) * time_epoch_unit

        # TODO 時間應該要來自網頁內容

        data_obj = json.dumps( {
            'url': item.get('url'),
            'title': item.get('title'),
            'tags': item.get('tags'),
            'text': item.get('text'),
            'time_epoch': time_epoch
        }, ensure_ascii=False )

        spider.redis_client.lpush('ckiptagger_worker_queue', data_obj)

        # spider.redis_client.set(time_epoch, data_obj, ex=daily_sec)

        return item
