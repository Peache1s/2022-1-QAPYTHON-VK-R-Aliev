import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from models import Base


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

    def connect(self, db_created = True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()
        session = sessionmaker(bind = self.connection.engine)
        self.session = session()

    def create_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')
        self.execute_query(f'CREATE database {self.db_name}')

    def drop_db(self):
        self.execute_query(f'DROP database IF EXISTS {self.db_name}')

    def execute_query(self, query, fetch = False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def create_table_number_of_requests(self):
        if not inspect(self.engine).has_table('number_of_requests'):
            Base.metadata.tables['number_of_requests'].create(self.engine)

    def create_table_requests_by_types(self):
        if not inspect(self.engine).has_table('requests_by_types'):
            Base.metadata.tables['requests_by_types'].create(self.engine)

    def create_table_most_requested(self):
        if not inspect(self.engine).has_table('most_requested'):
            Base.metadata.tables['most_requested'].create(self.engine)

    def create_table_top_users_with_server_error(self):
        if not inspect(self.engine).has_table('top_users_with_server_error'):
            Base.metadata.tables['top_users_with_server_error'].create(self.engine)

    def create_table_top_requests_with_client_error(self):
        if not inspect(self.engine).has_table('top_requests_with_client_error'):
            Base.metadata.tables['top_requests_with_client_error'].create(self.engine)