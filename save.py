from src.logger_handle import *
# from src.CassandraDatabase import CassandraDatabase

# db = CassandraDatabase('test')

import os
import time
import re
import json

now = int(time.time())
# DEBUG WARNING INFO
logger_handle(level=logging.DEBUG,
              logger_file='log/save-%s.log' % str(now))

for file_name in os.listdir('tmp/'):
    if re.match(r'^[\w]*-[0-9]{10}.json$', file_name):
        file_time = file_name.split('.')[0].split('-')[1]
        if now - int(file_time) > 5 * 60:
            logging.debug('Process file: %s' % file_name)

            with open('tmp/%s' % file_name, 'r') as f:
                data_rows = json.loads( f.read() )

            for row in data_rows:
                logging.debug('Row data url: %s' % row['url'])
                print(row['url'])
            # 讀檔案
            # 判斷內容hash
            # 塞 - 直接塞
            # 塞 - version2
            # 不塞 - 下一位
            # 處理完就刪除檔案

# logging.debug('')
# logging.info('')
# logging.warning('')
# logging.error('')
# logging.critical('')
'''
method 1
setp 1  read file from tmp
        if last file (now - timestamp) < N.sec skip
setp 2  check data.
        - prser text
        - insert db if row data not exist
        - if exist, check same, if not save version 2
Q.

method 2
setp 1  scrapy feed export item to amqp
setp 2  use amqp recive and write in db.(liken method 1)
'''
