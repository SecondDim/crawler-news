# /bin/python3
# -*- coding: utf-8 -*-

import sys
import time
import datetime
import re

import requests
from bs4 import BeautifulSoup
from retry import retry

# import sqlite3
from pony.orm import *
from src.db_model import *

from src.logger_handle import *
import sys


class ETTODAY(object):
    website = 'ettoday'
    base_url = 'https://www.ettoday.net'
    list_path = '/news/news-list-%s-%s.htm'

    error_msg = {'url': '', 'code': '', 'reason': ''}

    # TODO Like a general user
    # Change IP is important issue more than use-agent
    headers = {
        'User-Agent':  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }

    def __init__(self, ):
        logging.debug('Initialize requests session.')
        self.sreq = requests.Session()

        logging.debug('Session header: %s' % self.headers)
        self.sreq.headers.update(self.headers)

        logging.debug('Connect database to sqlite3')
        self._sqlite_connect('tmp/db.sqlite3')

        # logging.debug('Connect database to mysql')
        # self._mysql_connect(host='', user='', passwd='', db='')

    def _sqlite_connect(self, db_name):
        self.db = db_model
        self.db.bind(provider='sqlite', filename=db_name, create_db=True)
        self.db.generate_mapping(create_tables=True)

    def _mysql_connect(self, host='', user='', passwd='', db=''):
        self.db = db_model
        self.db.bind(provider='mysql', host='', user='', passwd='', db='')
        self.db.generate_mapping(create_tables=True)

    def _set_error_msg(self, rep):
        self.error_msg['url'] = rep.url
        self.error_msg['code'] = rep.status_code
        self.error_msg['reason'] = rep.reason

        return True

    @retry(tries=10, delay=3, logger=logging)
    def _get(self, url, payload={}):
        rep = self.sreq.get(url, params=payload)
        self._set_error_msg(rep)
        return rep

    @retry(tries=10, delay=3, logger=logging)
    def _post(self, url, payload={}):
        rep = self.sreq.get(url, data=payload)
        self._set_error_msg(rep)
        return rep

    def get_news_list(self, date, page):
        list_path = self.list_path % (date, page)
        rep = self._get(self.base_url + list_path)
        logging.info('Request website url: %s' % rep.url)
        logging.debug('Request website status: %s' % rep.status_code)
        logging.debug('Request website reason: %s' % rep.reason)

        soup = BeautifulSoup(rep.text, 'lxml')
        try:
            all_news_list = soup.find_all(class_='part_list_2')[0].find_all('h3')
        except AttributeError as e:
            logging.critical('BeautifulSoup analyze fails. : %s' % e)
            logging.error('Error Msg' % self.error_msg)
            raise
        except:
            e = sys.exc_info()[0]
            logging.critical('%s' % e)
            logging.error('Error Msg' % self.error_msg)
            raise

        return all_news_list

    def update_news_list(self, ):
        all_news_list = self.get_news_list(time.strftime('%Y-%m-%d'), '0')

        with db_session:
            for news in all_news_list:
                news_url = news.find('a').attrs['href']
                if QueueUrlEttoday.get(url=news_url) == None:
                    logging.info('Insert QueueUrlEttoday.url: %s' % news_url)
                    QueueUrlEttoday(url=news_url, fetch_state=False)

    def _parser_news_tags(self, soup, label):
        tag_label = []
        try:
            tags = soup.find(class_=label).find_all('a')
            for x in tags:
                tag_label.append(x.text)
            logging.info( 'BeautifulSoup get tags [%s] : %s' % (label, str(tag_label)) )
        except AttributeError as e:
            tag_label = []
            logging.error('BeautifulSoup get tag [%s] fails.' % label)
            logging.error('Error Msg' % self.error_msg)

        return tag_label


    def get_news(self, url):
        rep = self._get(self.base_url + url)
        logging.info('Request website url: %s' % rep.url)
        logging.debug('Request website status: %s' % rep.status_code)
        logging.debug('Request website reason: %s' % rep.reason)

        news_url = rep.url

        soup = BeautifulSoup(rep.text, 'lxml')
        # ! TODO 文章時間
        # TODO 標題 bs4 方法不同需要檢查
        try:
            news_title = soup.h1.text
            logging.debug('BeautifulSoup get title: %s' % news_title)
        except AttributeError as e:
            news_title = ""
            logging.error('BeautifulSoup get title fails. : %s' % rep.url)
            logging.error('Error Msg' % self.error_msg)

        news_tags = []
        if re.match('https://www.', rep.url):
            news_tags = news_tags + self._parser_news_tags(soup, 'part_menu_5')
            news_tags = news_tags + self._parser_news_tags(soup, 'part_tag_1')
        elif re.match('https://star.', rep.url):
            news_tags = news_tags + self._parser_news_tags(soup, 'menu_txt_2')
        elif re.match('https://fashion.', rep.url):
            news_tags = news_tags + self._parser_news_tags(soup, 'part_keyword')
        elif re.match('https://pets.', rep.url) \
                or re.match('https://sports.', rep.url)\
                or re.match('https://house.', rep.url)\
                or re.match('https://travel.', rep.url)\
                or re.match('https://health.', rep.url)\
                or re.match('https://speed.', rep.url)\
                or re.match('https://discovery.', rep.url):
            news_tags = news_tags + self._parser_news_tags(soup, 'tag')
        elif re.match('https://forum.', rep.url):
            news_tags = news_tags + self._parser_news_tags(soup, 'part_tag')
        else:
            logging.error('BeautifulSoup get website tags fails. : %s' % rep.url)
            logging.error('Error Msg' % self.error_msg)

        logging.debug('BeautifulSoup get tags: %s' % str(news_tags))

        try:
            news_html = soup.find(class_='story')
        except AttributeError as e:
            logging.error('BeautifulSoup get content fails. : %s' % e)
            logging.error('Error Msg' % self.error_msg)

        news_text = ''
        news_imgs = {}
        news_links = {}

        for p in news_html.find_all('p'):
            news_text += p.text

            tag_imgs = p.find_all('img')
            for img in tag_imgs:
                news_imgs[img.attrs['src']] = img.attrs['alt']

            tag_as = p.find_all('a')
            for a in tag_as:
                news_links[a.attrs['href']] = a.text


        logging.debug('bs4 get news_text: %20s' % news_text)
        logging.debug('bs4 get news_imgs: %20s' % news_imgs)
        logging.debug('bs4 get news_links: %20s' % news_links)

        return (news_url, news_title, news_tags, str(news_html), news_text, news_imgs, news_links)


    def update_news_article(self, limit=1000):

        with db_session:
            queue_url_ettoday_list = \
                QueueUrlEttoday.select(lambda f: not f.fetch_state)[:limit]

        for queue_url in queue_url_ettoday_list:

            time.sleep(5)

            news_url, news_title, news_tags, news_html, news_text, news_imgs, news_links = \
                self.get_news(queue_url.url)

            with db_session:
                article = Article(url=news_url, website=self.website,
                                  tags=news_tags, title=news_title,
                                  html=news_html, text=news_text)
                try:
                    logging.info('Insert Article: %s' % news_url)
                    commit()
                except TransactionIntegrityError as e:
                    logging.error('Insert Article Fails: %s' % news_url)
                    logging.error('Error Msg' % self.error_msg)

            if article.id != None:
                with db_session:
                    for news_link, news_name in news_links.items():
                        article_links = ArticleLinks(
                            name=news_name, url=news_link, article=article.id)
                        try:
                            logging.info('Insert ArticleLinks.: %s' % news_link)
                            commit()
                        except TransactionIntegrityError as e:
                            logging.warning('Insert ArticleLinks Fails: %s' % news_link)

                with db_session:
                    for img_url, img_alt in news_imgs.items():
                        article_imgs = ArticleImages(
                            alt=img_alt, url=img_url, article=article.id)
                        try:
                            logging.info('Insert ArticleImages.: %s' % img_url)
                            commit()
                        except TransactionIntegrityError as e:
                            logging.warning('Insert ArticleImages Fails: %s' % img_url)

            with db_session:
                QueueUrlEttoday[queue_url.id].fetch_state = True
                QueueUrlEttoday[queue_url.id].fetch_date = time.strftime('%Y-%m-%d')

    def run(self,):
        # TODO daemonize
        self.update_news_list()

        self.update_news_article()

    def test(self,):
        # set_sql_debug(True)

        self.update_news_list()

        self.update_news_article()


if __name__ == "__main__":
    # DEBUG WARNING INFO
    logger_handle(level=logging.DEBUG, logger_file='tmp/%s.log' %
                  sys.argv[0].split('.')[0])

    ettoday = ETTODAY()
    ettoday.test()
