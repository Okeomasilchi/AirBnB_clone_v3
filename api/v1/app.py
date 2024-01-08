#!/usr/bin/python3

"""
default model for the flask app instance
"""


import os
from flask import Flask
from flask_cors import CORS
from json import dumps as js
from api.v1.views import amenity_views
from api.v1.views import app_views
from api.v1.views import city_views
from api.v1.views import place_views
from api.v1.views import review_views
from api.v1.views import state_views
from api.v1.views import user_views
from api.v1.views import amenity_place_views
from models import storage


app = Flask(__name__)


@app.after_request
def apply_caching(response):
    """
    setting the "Content-Type" header to
    "application/json".
    """
    response.headers["Content-Type"] = "application/json"

    return response


cors = CORS(app, origins="0.0.0.0")
url_prefix = '/api/v1'


app.register_blueprint(amenity_views, url_prefix=url_prefix)
app.register_blueprint(app_views, url_prefix=url_prefix)
app.register_blueprint(city_views, url_prefix=url_prefix)
app.register_blueprint(place_views, url_prefix=url_prefix)
app.register_blueprint(state_views, url_prefix=url_prefix)
app.register_blueprint(user_views, url_prefix=url_prefix)
app.register_blueprint(review_views, url_prefix=url_prefix)
app.register_blueprint(amenity_place_views, url_prefix=url_prefix)


@app.teardown_appcontext
def close(exc):
    """
    used to close a storage object.
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    returns a JSON response with an
    error message and a status code of 404.

    Args:
      error: The error parameter is the error
      message that will be returned in the response.

    Returns:
      a JSON response error message "Not found
      and a status code of 404.
    """
    return js({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, debug=True, threaded=True)
