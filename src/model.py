""" Model implementation - saves data to the database """
import os
import sys
import logging as log
import redis

#pylint: disable=logging-fstring-interpolation

def env_var(name, default):
    """Safely retrieve an env var, with a default"""
    return os.environ.get(name) if name in os.environ else default

REDIS_HOST = env_var("REDIS_HOST", '0.0.0.0')
REDIS_PORT = env_var("REDIS_PORT", '6379')
REDIS_DB = env_var("REDIS_DB", '0')
REDIS_PWD = env_var("REDIS_PWD", '')

# this is a pointer to the module object instance itself.
# pylint: disable=invalid-name
this = sys.modules[__name__]
this.tblprefix = "flights:"
this.redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, \
                              db=REDIS_DB, password=REDIS_PWD,
                              decode_responses=True)

def save_reservation(reservation):
    """Saves reservation into Redis database"""

    seat_num = reservation['seat_num']
    try:
        result = this.redis_conn.hsetnx(
            this.tblprefix + reservation['flight_id'],
            seat_num,
            reservation['customer_id'])
    except redis.RedisError:
        response = {
            "error" : f"Unexpected error reserving {seat_num}"
        }
        log.error(f"Unexpected error reserving {seat_num}", exc_info=True)
    else:
        if result == 1:
            response = {
                "status": "success",
            }
        else:
            response = {
                "error" : f"Could not complete reservation for {seat_num}",
                "description" : "Seat already reserved. Cannot double-book"
            }

    return response

def get_reservations(flight_id):
    """List of reservations for a flight, from Redis database"""
    try:
        key = this.tblprefix + flight_id
        reservations = this.redis_conn.hgetall(key)
    except redis.RedisError:
        response = {
            "error" : "Cannot retrieve reservations"
        }
        log.error("Error retrieving reservations from Redis",
                  exc_info=True)
    else:
        response = reservations
        log.info(f"reservations: {reservations}")

    return response
