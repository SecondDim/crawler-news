import requests
import re
import redis
import json

url = "https://docs.google.com/document/d/15BJg6eleAqn787BRk8pCMJtbnuQ_NUE9lZ4nWFm4lis/edit?usp=sharing"

r = requests.get(url)
if r.status_code != 200:
    raise "requests error."

m = re.search(r'=====START KEY WORD LIST=====[\w\W]*=====END KEY WORD LIST=====', r.text)

if m:
    key_words = m.group(0).split('//')[1].split(',')
    key_words = [i.strip() for i in key_words]

    redis_connect = redis.Redis(host='localhost', port=6379, db=0)
    redis_connect.set('key_words', json.dumps(key_words, ensure_ascii=False))
