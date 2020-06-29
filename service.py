"""Entry point of our microservice. API endpoints (routes) are defined here.
 """

#pylint: disable=unused-import
import logging as log
import uuid
import json

from flask import Flask, request, jsonify, Response
from src import handlers, model

# pylint: disable=invalid-name
app = Flask(__name__)


@app.route('/reservations', methods=['GET'])
def reservations():
    """ Get Reservations Endpoint"""
    flight_id = request.args.get('flight_id', '')
    resp = handlers.get_reservations(flight_id)
    return jsonify(resp)

@app.route('/reservations', methods=['PUT'])
def reserve():
    """Endpoint that reserves a seat for a customer"""
    json_body = request.get_json(force=True)
    resp = handlers.reserve(json_body)
    if resp.get("status") == "success":
        return jsonify(resp)

    return Response(
        json.dumps(resp),
        status=403,
        mimetype='application/json'
    )

@app.route('/ping', methods=['GET'])
def ping():
    """ Liveness probe """
    resp = {
        "status" : "pass"
    }
    return jsonify(resp)

def init():
    """Init routine for the microservice"""
    uuid.uuid1() # prime the uuid generator at startup

if __name__ == '__main__':
    init()

    app.run(debug=True, host='0.0.0.0')
