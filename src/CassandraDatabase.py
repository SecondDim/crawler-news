import cassandra
from cassandra.cluster import Cluster

class CassandraDatabase():
    def __init__(self, keyspace, table, host=['localhost']):
        self.keyspace = keyspace
        self.host = host
        self.table = table

        self.connect()

    def __del__(self,):
        self.cluster.shutdown()

    def connect(self,):
        self.cluster = Cluster(self.host)
        self.session = self.cluster.connect()
        self.create_keyspace()
        self.session.set_keyspace(self.keyspace)

    def close(self,):
        self.cluster.shutdown()

    def create_keyspace(self):
        sql = """
                SELECT keyspace_name
                FROM system_schema.keyspaces
                WHERE keyspace_name='%s'
            """ % self.keyspace

        if self.query(sql).one() == None:
            self.query("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % self.keyspace)

    def create_table(self,):
        sql = """
                CREATE TABLE IF NOT EXISTS %s (
                    url varchar, article_from varchar, article_type varchar,
                    title varchar, publish_date varchar, authors list<varchar>,
                    tags list<varchar>, text_ list<varchar>, text_html text,
                    images list<varchar>, video list<varchar>, links list<varchar>,
                PRIMARY KEY(url)
                    );
            """ % self.table
        self.query(sql)

        sql = """
                CREATE INDEX IF NOT EXISTS ON %s(article_from);
            """ % self.table
        self.query(sql)

        sql = """
                CREATE INDEX IF NOT EXISTS ON %s(article_type);
            """ % self.table
        self.query(sql)

    def query(self, sql, args=None):
        return self.session.execute(sql, args)

    def fetchOne(self, url):
        sql = """
                SELECT *
                FROM %s
                WHERE url='%s'
            """ % (self.table, url)

        return self.query(sql).one()

    def insert(self, data={}):
        sql = "INSERT INTO %s "% (self.table)
        sql = sql + """
                (url, article_from, article_type,
                 title, publish_date, authors, tags,
                 text_, text_html, images, video, links)
                VALUES
                (%(url)s, %(article_from)s, %(article_type)s,
                 %(title)s, %(publish_date)s, %(authors)s, %(tags)s,
                 %(text)s, %(text_html)s, %(images)s, %(video)s, %(links)s)
            """

        return self.query(sql, data)


    def update(self,):
        raise 'Method not implemented.'

    def delete(self,):
        raise 'Method not implemented.'
