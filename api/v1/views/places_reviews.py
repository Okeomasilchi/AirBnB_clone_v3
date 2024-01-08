#!/usr/bin/python3


"""
Models for the routes of the reviews_views
"""


from flask import abort, request
from json import dumps as js
from api.v1.views import review_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@review_views.route('places/<review_id>/reviews',
                    methods=['GET'], strict_slashes=False)
def get_review_by_place(review_id):
    """
    Retrieves all reviews associated with a specific place ID.
    """
    if not storage.get(Place, review_id):
        abort(404)

    return js([
        storage.get(Review, id).to_dict()
        for id in [review[7:]
                   for review in storage.all(Review)
                   ]
        if storage.get(Review, id).to_dict()["place_id"] == review_id])


@review_views.route('/reviews/<review_id>',
                    methods=['GET'], strict_slashes=False)
def single_review(review_id):
    """
    Retrieves a single review from storage and returns
    it as a JSON object.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return js(review.to_dict())


@review_views.route('/reviews/<review_id>',
                    methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    deletes a review from storage based on the
    provided review ID.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    review.delete()
    storage.save()

    return js({}), 200


@review_views.route('places/<place_id>/reviews',
                    methods=['POST'], strict_slashes=False)
def create_review_by_place(place_id):
    """
    creates a review for a specific place, given the place ID
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()

    if "user_id" not in data:
        return js({"error": "Missing user_id"}), 400

    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)

    if "text" not in data:
        return js({"error": "Missing text"}), 400

    data["place_id"] = place_id

    instance = Review(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@review_views.route('reviews/<review_id>',
                    methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    updates a review by retrieving it from storage, validating
    the request data, removing unnecessary fields, updating
    the review object with the new data, saving the changes,
    and returning the updated review as JSON.
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("place_id", None)
    data.pop("user_id", None)

    for key, value in data.items():
        setattr(review, key, value)

    review.save()
    return js(review.to_dict()), 200
