#!/usr/bin/python3

"""
Models for the routes of the amenity_place_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import amenity_place_views
from models import storage, storage_t
from models.place import Place
from models.amenity import Amenity
from models.state import State
from models.city import City


@amenity_place_views.route('places/<place_id>/amenities',
                           methods=['GET'], strict_slashes=False)
def get_amenity_by_place(place_id):
    """
    Retrieves the amenities associated with a
    given place ID.
    """
    if not storage.get(Place, place_id):
        abort(404)

    if storage_t == "db":
        return js([
            i.to_dict()
            for i in storage.get(Place, place_id).amenities
            ])
    else:
        return storage.get(Place, place_id).amenities


@amenity_place_views.route('places/<place_id>/amenities/<amenity_id>',
                           methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """
    The function deletes an amenity from a place.
    """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place:
        abort(404)

    if not amenity:
        abort(404)

    place.amenities.remove(amenity)
    place.save()

    return js({}), 200


@amenity_place_views.route('places/<place_id>/amenities/<amenity_id>',
                           methods=['POST'], strict_slashes=False)
def Link_amenity_to_place(place_id, amenity_id):
    """
    links an amenity to a place by adding the
    amenity to the place's list of amenities
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if amenity in place.amenities:
        return js(amenity.to_dict()), 200

    place.amenities.append(amenity)
    place.save()

    return js(amenity.to_dict()), 201
