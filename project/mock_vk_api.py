import threading
from flask import Flask, jsonify, request, make_response
import random


app = Flask(__name__)
vk_data = {}
import json


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_surname(username):
    print(request.headers)
    try:
        if vk_id := vk_data.get(username):
            data = {username: vk_id}
            data = json.dumps(data)
            res = make_response()
            res.headers['Status'] = '200 OK'
            res.headers['Content-Type'] = 'application/json'
            res.headers['Response'] = data
            return res
            #return jsonify({username : vk_id}), 200
        else:
            vk_id = random.randint(1, 100)
            vk_data[username] = vk_id
            data = {username: vk_id}
            data = json.dumps(data)
            res = make_response()
            res.headers['Status'] = '200 OK'
            res.headers['Content-Type'] = 'application/json'
            res.headers['Response'] = data
            return res
            #return jsonify({username : vk_id}), 200
    except:
        return jsonify({}), 404


def shutdown_stub():
    terminate_func = request.environ.get('werkzeug.server.shutdown')
    if terminate_func:
        terminate_func()


@app.route('/shutdown')
def shutdown():
    shutdown_stub()
    return jsonify(f'Ok, exiting'), 200


def run_mock():
    server = threading.Thread(target=app.run, kwargs={
        'host': '0.0.0.0',
        'port': '8008'
    })

    server.start()
    return server


run_mock()
