import pymysql.cursors

class MysqlDatabase():
    def __init__(self, host, user, password, db, table='test', charset='utf8mb4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = db
        self.table = table
        self.charset = charset
        self.connect()

    def __del__(self,):
        if self.connection.open:
            self.connection.close()

    def connect(self,):
        self.connection = pymysql.connect(
            host=self.host, user=self.user, password=self.password,
            charset=self.charset, cursorclass=pymysql.cursors.DictCursor)

        self.create_db()
        self.connection.select_db(self.database)
        self.create_table()

    def close(self,):
        self.connection.close()

    def query(self, sql, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)

    def execute(self, sql, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
        self.connection.commit()

    def fetch_one(self, sql, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(sql, params)
            result = cursor.fetchone()

        return result

    def create_db(self,):
        sql = "SHOW DATABASES LIKE '%s';" % self.database
        if self.fetch_one(sql) is None:
            sql = "CREATE DATABASE IF NOT EXISTS `%s`;" % self.database
            self.query(sql)

    def create_table(self,):
        sql = "SHOW TABLES LIKE '%s';" % self.table
        if self.fetch_one(sql) is None:
            sql = """
                CREATE TABLE IF NOT EXISTS `%s`.`%s` (
                    `id` serial NOT NULL AUTO_INCREMENT,
                    `url` varchar(255) NOT NULL,
                    `article_from` varchar(255) NOT NULL DEFAULT 'UNKNOWN',
                    `article_type` varchar(255) DEFAULT NULL,
                    `title` varchar(255) DEFAULT NULL,
                    `publish_date` varchar(255) DEFAULT NULL,
                    `authors` json DEFAULT NULL,
                    `tags` json DEFAULT NULL,
                    `text` text DEFAULT NULL,
                    `text_html` text DEFAULT NULL,
                    `images` json DEFAULT NULL,
                    `video` json DEFAULT NULL,
                    `links` json DEFAULT NULL,
                    `created_at` datetime NOT NULL DEFAULT NOW(),
                    `updated_at` datetime NOT NULL DEFAULT NOW(),
                    `deleted_at` datetime DEFAULT NULL,
                    PRIMARY KEY (id),
                    UNIQUE INDEX USING BTREE (url),
                    INDEX USING BTREE (title),
                    INDEX USING BTREE (article_from),
                    INDEX USING BTREE (article_type),
                    INDEX USING BTREE (created_at),
                    INDEX USING BTREE (updated_at),
                    INDEX USING BTREE (deleted_at)
                    ) ENGINE=InnoDB;
                """

            self.execute(sql % (self.database, self.table))

    def news_exist(self, url):
        sql = "SELECT * FROM %s.%s WHERE url='%s';"
        if self.fetch_one(sql % (self.database, self.table, url)) is None:
            return False
        return True

    def insert(self, data={}):
        sql = "INSERT INTO `%s`.`%s` " % (self.database, self.table)
        sql = sql + """
                (url, article_from, article_type,
                 title, publish_date, authors, tags,
                 text, text_html, images, video, links)
                VALUES
                (%(url)s, %(article_from)s, %(article_type)s,
                 %(title)s, %(publish_date)s, %(authors)s, %(tags)s,
                 %(text)s, %(text_html)s, %(images)s, %(video)s, %(links)s)
            """

        return self.execute(sql, data)

    def update(self,):
        raise 'Method not implemented.'

    def delete(self,):
        raise 'Method not implemented.'
