#!/usr/bin/python3

"""
default model for the flask app instance
"""

import unittest
from flask import Flask
import pytest
from api.v1.app import app


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    #app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_landing_aliases(client):
    landing = client.get("http://0.0.0.0:5000/api/vi/status")
    assert client.get("http://0.0.0.0:5000/api/vi/status").data == landing.data