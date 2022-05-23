import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData


class MysqlClient:

    def __init__(self, db_name, user, password):
        self.user = user
        self.port = 3306
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name
        self.connection = None
        self.engine = None
        self.session = None
        self.TestUsers = None

    def connect(self):
        db = self.db_name
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        Base = declarative_base()
        metadata = MetaData(bind=self.engine)
        class TestUsers(Base):
            __table__ = Table('test_users', metadata, autoload=True)
        self.TestUsers = TestUsers
        self.connection = self.engine.connect()
        session = sessionmaker(bind = self.connection.engine)
        self.session = session()


    def drop_db(self):
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')


    def execute_query(self, query, fetch = False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()
