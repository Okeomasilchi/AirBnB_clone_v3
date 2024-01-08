#!/usr/bin/python3

"""
Models for the routes of the User_views
"""


from flask import abort, request
from hashlib import md5
from json import dumps as js
from api.v1.views import user_views
from models import storage
from models.user import User


@user_views.route('/users',
                  methods=['GET'], strict_slashes=False)
def get_all_users():
    """
    Retrieves all users from storage and returns a list
    of their dictionaries.
    """
    users = storage.all(User)
    return js([
        storage.get(User, id).to_dict()
        for id in [
            user[5:]
            for user in users
            ]
        ])


@user_views.route('/users/<user_id>',
                  methods=['GET'], strict_slashes=False)
def get_single_user(user_id):
    """
    Retrieves a single user from storage based on their
    user ID and returns the user's information in JSON format.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return js(user.to_dict())


@user_views.route('/users/<user_id>',
                  methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """
    deletes a user from storage based on their user ID.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    user.delete()
    storage.save()
    return js({}), 200


@user_views.route('/users',
                  methods=['POST'], strict_slashes=False)
def create_new_user():
    """
    creates a new user by extracting data from a
    JSON request, hashing, the password, creating a
    new User instance, and saving it to storage.
    """
    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    if "email" not in data:
        return js({"error": "Missing email"}), 400
    if "password" not in data:
        return js({"error": "Missing password"}), 400

    if "password" in data:
        data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    instance = User(**data)
    storage.new(instance)
    storage.save()
    return js(instance.to_dict()), 201


@user_views.route('/users/<user_id>',
                  methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """
    updates a user's information in a storage system,
    including hashing the password if provided.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if not request.is_json:
        return js({"error": "Not a JSON"}), 400

    data = request.get_json()
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    data.pop("email", None)
    if "password" in data:
        data["password"] = md5(data.pop("password", None).encode()).hexdigest()

    for key, value in data.items():
        setattr(user, key, value)

    user.save()
    return js(user.to_dict()), 200
