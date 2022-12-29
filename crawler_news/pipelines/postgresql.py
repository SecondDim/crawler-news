# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import psycopg2

# # Connect to your postgres DB
# conn = psycopg2.connect("dbname=test user=postgres")

# # Open a cursor to perform database operations
# cur = conn.cursor()

# # Execute a query
# cur.execute("SELECT * FROM my_data")

# # Retrieve query results
# records = cur.fetchall()

class PostgresqlPipeline:
    def open_spider(self, spider):
        settings = spider.settings
        print('[pipelines] PostgresqlPipeline open_spider')
        # self.db = psycopg2.connect("dbname=crawler_news user=crawler_news")
        # self.db = MysqlDatabase(host=settings['MYSQL_HOST'],
        #                      port=settings['MYSQL_PORT'],
        #                      user=settings['MYSQL_USER'],
        #                      password=settings['MYSQL_PASSWORD'],
        #                      db=settings['MYSQL_DB'],
        #                      table=settings['MYSQL_TABLE'],
        #                      charset=settings['MYSQL_CHARSET'])

    def close_spider(self, spider):
        # self.db.close()
        print('[pipelines] PostgresqlPipeline close_spider')
        pass

    def process_item(self, item, spider):
        print('[pipelines] PostgresqlPipeline process_item')
        pass
