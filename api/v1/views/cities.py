#!/usr/bin/python3

"""
Models for the routes of the city_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import city_views
from models import storage
from models.city import City
from models.state import State


@city_views.route('/states/<state_id>/cities',
                  methods=['GET'], strict_slashes=False)
def get_city_by_state(state_id):
    """
    Retrieves a list of cities based on a given state ID.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return js([city.to_dict() for city in state.cities])


@city_views.route('/cities/<city_id>',
                  methods=['GET'], strict_slashes=False)
def single_city(city_id):
    """
    Retrieves a city object from storage based on its ID,
    and returns the city object as a JSON response.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return js(city.to_dict())


@city_views.route('/cities/<city_id>',
                  methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    deletes a city from storage based on its ID.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    city.delete()
    storage.save()

    return js({}), 200


@city_views.route('/states/<state_id>/cities',
                  methods=['POST'], strict_slashes=False)
def create_city_by_state(state_id):
    """
    creates a new city object associated with a given state.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400
    data = request.get_json()
    if "name" not in data:
        return js({"error": "Missing name"}), 400

    data["state_id"] = state_id
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    instance = City(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@city_views.route('/cities/<city_id>',
                  methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """
    updates the attributes of a city object with the
    provided data and returns the updated city object as JSON.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("state_id", None)

    for key, value in data.items():
        setattr(city, key, value)

    city.save()
    return js(city.to_dict()), 200
