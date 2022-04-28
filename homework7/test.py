import pytest


class TestClass:

    def test_post(self, client):
        data = client.post('audi', 'white')
        assert data.split()[1]==str(201)

    def test_negative_post(self, client):
        client.post('BMW', 'white')
        data = client.post('BMW', 'white')
        assert data.split()[1]==str(400)

    def test_get(self, client):
        client.post('Lada', 'green')
        data = client.get('Lada')
        assert data.split()[1] == str(200)

    def test_negative_get(self, client):
        client.post('Volga', 'green')
        data = client.get('Bugatti')
        assert data.split()[1] == str(404)

    def test_put(self, client):
        client.post('Mazda', 'red')
        data = client.put('Mazda', 'blue')
        assert data.split()[1] == str(200)

    def test_put_create(self, client):
        data = client.put('Nissan', 'blue')
        assert data.split()[1] == str(201)

    def test_negative_delete(self, client):
        data = client.delete('KIA', 'white')
        assert data.split()[1] == str(404)

    def test_negative_delete(self, client):
        client.post('Renault', 'grey')
        data = client.delete('Renault')
        assert data.split()[1] == str(200)