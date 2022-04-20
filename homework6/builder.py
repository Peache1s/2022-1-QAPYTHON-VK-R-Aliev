from models import NumberOfRequests, RequestsByTypes, MostRequested, ServerError, ClientError


class MysqlBuilder:
    def __init__(self, client):
        self.client = client

    def add_data_to_number_of_requests(self, number):
        self.client.create_table_number_of_requests()
        number_for_add = number
        number_of_requests = NumberOfRequests(number=number_for_add)
        self.client.session.add(number_of_requests)
        self.client.session.commit()
        return number_of_requests

    def add_data_to_requests_by_types(self, data):
        self.client.create_table_requests_by_types()
        for i in range(len(data[0])):
            requests_by_types = RequestsByTypes(
                type=data[0][i],
                number=data[1][i]
            )
            self.client.session.add(requests_by_types)
            self.client.session.commit()
        return len(data[0])

    def add_data_to_most_requested(self, data):
        self.client.create_table_most_requested()
        for key, value in data.items():
            most_requested = MostRequested(
                url=key,
                number=value
            )
            self.client.session.add(most_requested)
            self.client.session.commit()
        return len(data)

    def add_data_to_server_error(self, data):
        self.client.create_table_top_users_with_server_error()
        for key, value in data.items():
            top_users_with_server_error = ServerError(
                ip=key,
                number=value
            )
            self.client.session.add(top_users_with_server_error)
            self.client.session.commit()
        return len(data)

    def add_data_to_client_error(self, data):
        self.client.create_table_top_requests_with_client_error()
        for i in range(len(data)):
            top_requests_with_client_error = ClientError(
                size=data[i][0],
                ip=data[i][1][0],
                code=data[i][1][1],
                url=data[i][1][2]
            )
            self.client.session.add(top_requests_with_client_error)
            self.client.session.commit
        return len(data)