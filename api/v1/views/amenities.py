#!/usr/bin/python3

"""
Models for the routes of the amenity_views
"""

from flask import abort, request
from json import dumps as js
from api.v1.views import amenity_views
from models import storage
from models.amenity import Amenity


@amenity_views.route('/amenities', methods=['GET'],
                     strict_slashes=False)
def get_all_amenities():
    """
    Retrieves all amenities from storage and returns
    them as a list of dictionaries.

    Returns:
      a JavaScript array of dictionaries.
    """
    amenities = storage.all(Amenity)
    return js([
        storage.get(Amenity, id).to_dict()
        for id in [
            amenity[8:]
            for amenity in amenities
            ]
        ])


@amenity_views.route('/amenities/<amenity_id>',
                     methods=['GET'], strict_slashes=False)
def get_single_amenity(amenity_id):
    """
    Retrieves a single amenity object

    Args:
      amenity_id: unique identifier of the amenity that
      we want to retrieve from the storage.

    Returns:
      JSON representation of the amenity object
      with the given amenity_id.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return js(amenity.to_dict())


@amenity_views.route('/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    deletes an amenity object from storage based on its ID.

    Args:
      amenity_id: unique identifier of the amenity that
      needs to be deleted.

    Returns:
      empty JSON object and a status code of 200.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    amenity.delete()
    storage.save()
    return js({}), 200


@amenity_views.route('/amenities',
                     methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """
    Creates a new Amenity object using data from a
    JSON request and saves it to storage.

    Returns:
      The code is returning a JSON response.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "name" not in data:
        return js({"error": "Missing name"}), 400

    instance = Amenity(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@amenity_views.route('/amenities/<amenity_id>',
                     methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates the attributes of an amenity object with
    the provided data and returns the updated amenity
    as a JSON response.

    Args:
      amenity_id: unique identifier of the amenity that
      needs to be updated.

    Returns:
      a JSON response with the updated amenity data
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)

    for key, value in data.items():
        setattr(amenity, key, value)

    amenity.save()
    return js(amenity.to_dict()), 200
