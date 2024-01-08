#!/usr/bin/python3


"""
Models for the routes of the place_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import place_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@place_views.route('cities/<city_id>/places',
                   methods=['GET'], strict_slashes=False)
def get_place_by_city(city_id):
    """
    Retrieves a list of places based on a given city ID.
    """
    if not storage.get(City, city_id):
        abort(404)

    places = storage.all(Place)

    return js([
        storage.get(Place, id).to_dict()
        for id in [
            place[6:] for place in places
            ]
        if storage.get(Place, id).to_dict()["city_id"] == city_id])


@place_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    """
    Retrieves a place object from storage based on its ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return js(place.to_dict())


@place_views.route('/places/<place_id>',
                   methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    deletes a place from storage based on its ID.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    place.delete()
    storage.save()

    return js({}), 200


@place_views.route('cities/<city_id>/places',
                   methods=['POST'], strict_slashes=False)
def create_place_by_city(city_id):
    """
    creates a new place in a city based on the provided city
    ID, user ID, and place name.
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()

    if "user_id" not in data:
        return js({"error": "Missing user_id"}), 400

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "name" not in data:
        return js({"error": "Missing name"}), 400

    data["city_id"] = city_id

    instance = Place(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@place_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    updates a place object with new data provided in a
    JSON format.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("city_id", None)
    data.pop("user_id", None)

    for key, value in data.items():
        setattr(place, key, value)

    place.save()
    return js(place.to_dict()), 200
