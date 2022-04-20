import pytest
from client import MysqlClient
from builder import MysqlBuilder
from models import NumberOfRequests, RequestsByTypes, MostRequested, ServerError
from scripts_from_hw5.number_of_requests import numb_of_req
from scripts_from_hw5.requests_by_types import req_by_types
from scripts_from_hw5.most_requested import most_req
from scripts_from_hw5.server_error_requests import server_error
from scripts_from_hw5.client_error_requests import client_error


class MyTest:

    @pytest.fixture(scope = 'function', autouse = True)
    def setup(self, mysql_client):
        self.mysql: MysqlClient = mysql_client
        self.builder: MysqlBuilder = MysqlBuilder(self.mysql)


class TestMySql(MyTest):

    def test_number_of_requests(self):
        self.builder.add_data_to_number_of_requests(numb_of_req())
        self.mysql.session.commit()
        rows = self.mysql.session.query(NumberOfRequests).count()
        assert rows == 1

    def test_requests_by_types(self):
        self.builder.add_data_to_requests_by_types(req_by_types())
        self.mysql.session.commit()
        rows = self.mysql.session.query(RequestsByTypes).count()
        assert rows == len(req_by_types()[0])

    def test_most_requested(self):
        self.builder.add_data_to_most_requested(most_req())
        self.mysql.session.commit()
        rows = self.mysql.session.query(MostRequested).count()
        assert rows == len(most_req())

    def test_top_users_with_server_error(self):
        self.builder.add_data_to_server_error(server_error())
        self.mysql.session.commit()
        rows = self.mysql.session.query(ServerError).count()
        assert rows == len(server_error())

    def test_top_requests_with_client_error(self):
        self.builder.add_data_to_client_error(client_error())
        self.mysql.session.commit()
        rows = self.mysql.session.query(ServerError).count()
        assert rows == len(client_error())