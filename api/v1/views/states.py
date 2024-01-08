#!/usr/bin/python3

"""
Models for the routes of the state_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import state_views
from models import storage
from models.state import State


@state_views.route('/states',
                   methods=['POST'], strict_slashes=False)
def create_new_state():
    """
    creates a new state object using data from a JSON request
    and saves it to storage.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "name" not in data:
        return js({"error": "Missing name"}), 400

    instance = State(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@state_views.route('/states',
                   methods=['GET'], strict_slashes=False)
def get_all_state():
    """
    Retrieves all instances of the `State` class from
    storage and returns them as a list of dictionaries.
    """
    states = storage.all(State)
    return js([
        storage.get(State, id).to_dict()
        for id in [
            state[6:]
            for state in states
            ]
        ])


@state_views.route('/states/<state_id>',
                   methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """
    Retrieves a single state object from storage
    and returns it as a JSON response.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return js(state.to_dict())


@state_views.route('/states/<state_id>',
                   methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    updates the state object with the provided state_id
    using the data from the JSON request.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(state, key, value)

    state.save()
    return js(state.to_dict()), 200


@state_views.route('/states/<state_id>',
                   methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    deletes a state object from storage based on its ID.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    state.delete()
    storage.save()

    return js({}), 200
