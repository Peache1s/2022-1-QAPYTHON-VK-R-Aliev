import time
from socket_client import Client
import pytest
import requests
import settings
import moсk_flask


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 15:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        moсk_flask.run_mock()
        wait_ready(settings.MOCK_HOST, int(settings.MOCK_PORT))


@pytest.fixture(scope='session',autouse=True)
def stop_server():
    yield
    requests.get(f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/shutdown')


@pytest.fixture()
def client():
    client = Client(settings.MOCK_HOST, int(settings.MOCK_PORT))
    client.run()
    yield client
    client.close()


@pytest.fixture(scope='session', autouse=True)
def clearing_log_file():
    with open("log_file.txt", 'w') as File:
        File.write("")