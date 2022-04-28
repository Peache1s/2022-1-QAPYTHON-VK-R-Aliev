import signal
import threading
import json
from flask import Flask, jsonify, request
import os
import settings


app = Flask(__name__)

CAR_DATA = {}

@app.route('/get_car_color/<car>', methods=['GET'])
def get_user_surname(car):
    print(car)
    if color := CAR_DATA.get(car):
        return jsonify(color), 200
    else:
        return jsonify(f'Car "{car}" not found'), 404

@app.route('/add_car', methods = ['POST'])
def create_user():
    data = json.loads(request.data)
    car = list(data.keys())[0]
    color = data[car]
    if car not in CAR_DATA:
        CAR_DATA[car] = color
        return jsonify({'color': CAR_DATA[car]}), 201

    else:
        return jsonify(f'Car already created, color =  {CAR_DATA[car]}'), 400

@app.route('/put_car', methods = ['PUT'])
def put_car():
    data = json.loads(request.data)
    car = list(data.keys())[0]
    color = data[car]
    if car not in CAR_DATA:
        CAR_DATA[car] = color
        return jsonify({'color': CAR_DATA[car]}), 201
    else:
        CAR_DATA[car] = color
        return jsonify({'color': CAR_DATA[car]}), 200

@app.route('/delete_car/<car>', methods = ['DELETE'])
def delete(car):
    if car not in CAR_DATA:
        return jsonify(f'Car {car} not found'), 404
    else:
        color = CAR_DATA[car]
        CAR_DATA.pop(car)
        return jsonify(f'Car {car} with color {color} deleted'), 200

def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


@app.route('/stopServer', methods = ['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({"success": True, "message": "Server is shitting down"})


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': settings.MOCK_HOST,
        'port': settings.MOCK_PORT
    })
    server.start()
    return server