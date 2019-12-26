import cassandra
from cassandra.cluster import Cluster

class CassandraDatabase():
    def __init__(self, keyspace, host=['localhost']):
        self.keyspace = keyspace
        self.host = host

        self.connect()

    def __del__(self,):
        self.cluster.shutdown()

    def connect(self,):
        self.cluster = Cluster(self.host)
        self.session = self.cluster.connect()
        self.create_keyspace()
        self.session.set_keyspace(self.keyspace)

    def create_keyspace(self):
        sql = """
                SELECT keyspace_name
                FROM system_schema.keyspaces
                WHERE keyspace_name='%s'
            """ % self.keyspace

        if self.session.execute(sql).one() == None:
            self.session.execute("""
                CREATE KEYSPACE %s
                WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
                """ % self.keyspace)

    def query(self, sql):
        return self.session.execute(sql)

    def fetchOne(self,):
        raise 'Method not implemented.'

    def insert(self,):
        raise 'Method not implemented.'

        # insert_sql = self.session.prepare("INSERT INTO  employee (emp_id, ename , sal,city) VALUES (?,?,?,?)")
        # batch = BatchStatement()
        # batch.add(insert_sql, (1, 'LyubovK', 2555, 'Dubai'))
        # batch.add(insert_sql, (2, 'JiriK', 5660, 'Toronto'))
        # batch.add(insert_sql, (3, 'IvanH', 2547, 'Mumbai'))
        # batch.add(insert_sql, (4, 'YuliaT', 2547, 'Seattle'))
        # self.session.execute(batch)
        # self.log.info('Batch Insert Completed')


    def update(self,):
        raise 'Method not implemented.'

    def delete(self,):
        raise 'Method not implemented.'

    def is_exist(self, table, where):
        sql = 'select * from %s where %s limit 1;' % (table, where)
        print( self.query(sql) )
        # if self.session.execute(sql).one() == None:
        return

# import cassandra
# from cassandra.cluster import Cluster

# KEYSPACE = "testkeyspace"

# cluster = Cluster()

# session = cluster.connect()

# rows = session.execute("SELECT * FROM system_schema.keyspaces")

# Row(  keyspace_name='system_auth',
#       durable_writes=True,
#       replication=OrderedMapSerializedKey(
#           [('class', 'org.apache.cassandra.locator.SimpleStrategy'),
#            ('replication_factor', '1')])
#     )
# for row in rows:
#     print(row)
    # print(row.keyspace_name)

# session.execute("""
#     CREATE KEYSPACE %s
#     WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
#     """ % keyspace)

# if keyspace in [row[0] for row in rows]:
    # log.info("dropping existing keyspace...")
    # session.execute("DROP KEYSPACE " + keyspace)

# session.execute('USE users')
# rows = session.execute('SELECT name, age, email FROM users')
# for user_row in rows:
#     print(user_row.name, user_row.age, user_row.email)
