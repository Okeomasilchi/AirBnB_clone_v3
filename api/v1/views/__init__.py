#!/usr/bin/python3

"""
Model that handles import and export of views
"""


from flask import Blueprint
from flask_cors import CORS

app_views = Blueprint('app_views', __name__)
state_views = Blueprint('state_views', __name__)
city_views = Blueprint('city_views', __name__)
amenity_views = Blueprint('amenity_views', __name__)
user_views = Blueprint('user_views', __name__)
place_views = Blueprint('place_views', __name__)
review_views = Blueprint('review_views', __name__)
amenity_place_views = Blueprint("amenity_place_views", __name__)

CORS(app_views)
CORS(state_views)
CORS(amenity_views)
CORS(city_views)
CORS(user_views)
CORS(place_views)
CORS(review_views)
CORS(amenity_place_views)

# Import all views in the package (wildcard import)
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
