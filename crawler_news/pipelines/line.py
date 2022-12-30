# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import requests
import re
import json

from scrapy.exceptions import DropItem

notify_key_words = 'notify_key_words'

class LineNotifyPipeline(object):

    def open_spider(self, spider):
        self.token = spider.settings.get('LINE_NOTIFY_TOKEN')

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

        key_words = json.loads(spider.redis_client.get(notify_key_words))

        conditions = ''
        if self._re(item['title'], key_words):
            conditions += '標題 包含關鍵字 [%s]\n' % self._re(item['title'], key_words)
        if self._re(item['tags'], key_words):
            conditions += '標籤 包含關鍵字 [%s]\n' % self._re(item['tags'], key_words)
        if self._re(item['text'], key_words):
            conditions += '內文 包含關鍵字 [%s]\n' % self._re(item['text'], key_words)

        if conditions != '':
            msg = "觸發條件：\n%s\n\n新聞標題：%s\n\n新聞網址：%s" % (conditions, item.get('title'), item.get('url'))
            self.line_notify_message(msg)
            spider.logger.info('Send line notify message. %s' % item.get('url'))

        return item
