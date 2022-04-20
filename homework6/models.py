from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class NumberOfRequests(Base):

    __tablename__ = 'number_of_requests'
    __table_args__ = {'mysql_charset': 'utf8'}

    number = Column(Integer, primary_key=True)


class RequestsByTypes(Base):

    __tablename__ = 'requests_by_types'
    __table_args__ = {'mysql_charset': 'utf8'}

    type = Column(String(10), primary_key=True)
    number = Column(Integer)


class MostRequested(Base):

    __tablename__ = 'most_requested'
    __table_args__ = {'mysql_charset': 'utf8'}

    url = Column(String(200), primary_key=True)
    number = Column(Integer)


class ServerError(Base):

    __tablename__ = 'top_users_with_server_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    ip = Column(String(25), primary_key=True)
    number = Column(Integer)


class ClientError(Base):

    __tablename__ = 'top_requests_with_client_error'
    __table_args__ = {'mysql_charset': 'utf8'}

    url = Column(String(300), primary_key=True)
    ip = Column(String(25))
    code = Column(Integer)
    size = Column(Integer)