# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import re
import redis
import json

from scrapy.exceptions import DropItem

class LineNotifyPipeline(object):

    def open_spider(self, spider):
        settings = spider.settings
        self.token = settings['LINE_NOTIFY_TOKEN']
        self.redis = redis.Redis(
                        host=settings['REDIS_HOST'],
                        port=settings['REDIS_PORT'],
                        db=settings['REDIS_DATABASE'])

    def close_spider(self, spider):
        pass

    def _re(self, targets, key_words):
        if type(targets) is str:
            targets = [targets]

        if type(targets) is list:
            for target in targets:
                for key_word in key_words:
                    match = re.search(key_word, target)
                    if match:
                        return match.group(0)

        return False

    def line_notify_message(self, msg):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type" : "application/x-www-form-urlencoded"
        }

        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)

        return r.status_code

    async def process_item(self, item, spider):
        if not item.get('url'):
            raise DropItem("Missing item.url in %s" % item)

        if self.redis.get(item.get('url')):
            return item

        # self.redis.set('key_words', json.dumps(['Hello world!'], ensure_ascii=False))

        key_words = json.loads(self.redis.get('key_words'))

        NOTIFY = False
        if self._re(item['title'], key_words):
            NOTIFY = True
            conditions = '標題 包含關鍵字 [%s]' % self._re(item['title'], key_words)
        elif self._re(item['tags'], key_words):
            NOTIFY = True
            conditions = '標籤 包含關鍵字 [%s]' % self._re(item['tags'], key_words)
        # elif self._re(item['text'], key_words):
        #     NOTIFY = True
        #     conditions = '內文 包含關鍵字 [%s]' % self._re(item['text'], key_words)

        if NOTIFY:
            msg = "觸發條件：%s\n\n新聞標題：%s\n\n新聞網址：%s" % (conditions, item.get('title'), item.get('url'))
            self.line_notify_message(msg)
            self.redis.set(item.get('url'), 'True', ex=86400)
            spider.logger.info('Send line notify message. %s' % item.get('url'))

        return item
