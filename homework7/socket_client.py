import json
import socket
import settings


class Client:
    url = f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}'

    def __init__(self, host = settings.MOCK_HOST, port = int(settings.MOCK_PORT) ):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
        self.host = host

    def run(self):
        self.socket.connect((self.host, self.port))

    def close(self):
        self.socket.close()

    def get(self, car, meth = '/get_car_color/'):
        params = meth + car
        request = f'GET {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'
        self.socket.send(request.encode())
        returning_data = self.socket.recv(1024).decode()
        self.response_handler_socket(returning_data)
        return returning_data

    def response_handler_socket(self, data):
        string = data.split('\n')
        if len(string) > 2:
            code = data.split()[1]
            headers = data.split("\n\r")[0]
            headers = headers.split('\n')[1::]
            body = data.split("\n\r")[1]
            with open('log_file.txt', "a") as FileLog:
                FileLog.write(f'CODE: {code}\n')
                FileLog.write(f'HEADERS:\n')
                for x in headers:
                    FileLog.write(x)
                    FileLog.write("\n")
                FileLog.write(f'BODY: {body}')
        else:
            body = data
            with open('log_file.txt', "a") as FileLog:
                FileLog.write(f'BODY: {body}')


    def post(self, car, color, meth = '/add_car'):
        len_of_data = 8 + len(car) + len(color)
        dict = {car: color}
        data = json.dumps(dict)
        request = "".join((f"POST {meth} HTTP/1.1\r\n",
                           f"Host: {self.host}:{self.port}\r\n",
                           "Accept-Encoding: gzip, deflate\r\n",
                           "Accept: */*\r\n",
                           "Connection: keep-alive\r\n",
                           "Content-Type: application/json\r\n",
                           f"Content-Length: {len_of_data}\r\n\r\n",
                           f'{data}'))

        self.socket.send(request.encode())
        returning_data = self.socket.recv(1024).decode()
        self.response_handler_socket(returning_data)
        return returning_data

    def put(self, car, color, meth = '/put_car'):
        len_of_data = 8 + len(car) + len(color)
        dict = {car: color}
        data = json.dumps(dict)
        request = "".join((f"PUT {meth} HTTP/1.1\r\n",
                           f"Host: {self.host}:{self.port}\r\n",
                           "Accept-Encoding: gzip, deflate\r\n",
                           "Accept: */*\r\n",
                           "Connection: keep-alive\r\n",
                           "Content-Type: application/json\r\n",
                           f"Content-Length: {len_of_data}\r\n\r\n",
                           f'{data}'))
        self.socket.send(request.encode())
        returning_data = self.socket.recv(1024).decode()
        print(returning_data)
        self.response_handler_socket(returning_data)
        return returning_data

    def delete(self, car, meth = '/delete_car/'):
        params = meth + car
        request = "".join((f"DELETE {params} HTTP/1.1\r\n",
                           f"Host: {self.host}:{self.port}\r\n\r\n"))
        self.socket.send(request.encode())
        returning_data = self.socket.recv(1024).decode()
        self.response_handler_socket(returning_data)
        return returning_data