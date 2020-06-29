""" Endpoint Callback Handlers """

#pylint: disable=unused-import
import logging as log
import uuid
import json

from . import model

def get_reservations(flight_id):
    """Get reservations callback"""
    return model.get_reservations(flight_id)

def reserve(json_body):
    """Save reservation callback"""
    return model.save_reservation(json_body)
