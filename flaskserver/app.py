from flask import Flask
from flask import request, jsonify
import json
import urllib.request
from functions import resolve_request

app = Flask(__name__)

def get(username, password):
    data = resolve_request(username, password)
    return jsonify(data)

@app.route('/', methods=['GET'])
def run():
    try:
        username = request.args['username']
        password = request.args['password']
    except:
        resp = {
            'error': 'No Username/Password provided'
        }
        data = jsonify(resp)
        data.headers.add('Access-Control-Allow-Origin', '*')
        return data
    try:
        data = get(username, password)
        data.headers.add('Access-Control-Allow-Origin', '*')
        return data
    except Exception as e:
        resp = {
            'error': e
        }
        data = jsonify(resp)
        data.headers.add('Access-Control-Allow-Origin', '*')
        return data


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
