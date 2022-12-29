# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import jieba.posseg as pseg
import jieba
# import paddle

# paddle.enable_static()
# jieba.enable_paddle()

from ckiptagger import data_utils, construct_dictionary, WS, POS, NER

class JiebaPipeline:
    def process_item(self, item, spider):
        text = item.get('text')
        for t in text:
            self._paddle_cut(t)
        # print(text)
        return item

    def _paddle_cut(self, test_sent):
        seg_list = jieba.cut(test_sent,use_paddle=True)
        print("Paddle Mode: " + '/'.join(list(seg_list)))
        # for word in list(seg_list):
        #     print('%s' % (word))

    def _default_cut(self, test_sent):
        seg_list = jieba.cut(test_sent, cut_all=False)
        print("Default Mode: " + "/ ".join(seg_list))

    def _full_cut(self, test_sent):
        seg_list = jieba.cut(test_sent, cut_all=True)
        print("Full Mode: " + "/ ".join(seg_list))
