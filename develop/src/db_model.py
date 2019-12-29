# -*- coding: utf-8 -*-

from datetime import datetime
from pony.orm import *

db_model = Database()


class QueueUrlEttoday(db_model.Entity):
    url = Required(str, unique=True)
    fetch_state = Required(bool)
    fetch_date = Optional(datetime, default=datetime.min)
    create_date = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    remark = Optional(str)


class Article(db_model.Entity):
    url = Required(str, unique=True)
    website = Required(str)
    tags = Optional(Json)
    title = Required(str)
    html = Required(LongStr)
    text = Required(LongStr)
    article_date = Required(datetime)
    create_date = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    links = Set("ArticleLinks")
    urls = Set("ArticleImages")
    remark = Optional(str)


class ArticleLinks(db_model.Entity):
    article = Required(Article)
    name = Optional(str)
    url = Required(str, unique=True)
    create_date = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    remark = Optional(str)


class ArticleImages(db_model.Entity):
    article = Required(Article)
    alt = Optional(str)
    url = Required(str, unique=True)
    create_date = Required(datetime, sql_default='CURRENT_TIMESTAMP')
    remark = Optional(str)
