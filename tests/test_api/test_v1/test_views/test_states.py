#!/usr/bin/python3

"""
Models for the routes of the state_views
"""


import json
from flask import Flask
import unittest
from api.v1.app import app


class Test_StateAPI(unittest.TestCase):
    """Test case for the StateAPI class."""

    def setUp(self):
        app.config['TESTING'] = True
        self.states_url = "http://0.0.0.0:5000/api/v1/states"
        self.client = app.test_client()

    def tearDown(self):
        app.teardown_appcontext

    def test_get_all_states(self):
        response = self.client.get(self.states_url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_specific_state(self):
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            response_specific_state = self.client.get(
                f"{self.states_url}/{state_id}")
            self.assertEqual(response_specific_state.status_code, 200)
            data_specific_state = response_specific_state.get_json()
            self.assertIsInstance(data_specific_state, dict)
            self.assertEqual(data_specific_state['id'], state_id)

    def test_get_nonexistent_state(self):
        response = self.client.get(f"{self.states_url}/nonexistent_state_id")
        self.assertEqual(response.status_code, 404)


class TestStates(unittest.TestCase):
    """Test case for the states API endpoints."""

    def setUp(self):
        """Set up the test environment before each test method is run."""
        app.config['TESTING'] = True
        self.states_url = "http://0.0.0.0:5000/api/v1/states"
        self.client = app.test_client()

    def tearDown(self):
        """Tear down the test environment after each test
        method has been run.
        """
        app.teardown_appcontext

    def test_delete_state(self):
        """Test deleting a state from the database."""
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            response_delete = self.client.delete(
                f"{self.states_url}/{state_id}")
            self.assertEqual(response_delete.status_code, 200)
            data_delete = response_delete.get_json()
            self.assertIsInstance(data_delete, dict)
            self.assertEqual(data_delete, {})

    def test_delete_nonexistent_state(self):
        response = self.client.delete(
            f"{self.states_url}/nonexistent_state_id"
            )
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        state_data = {"name": "New State"}
        response = self.client.post(self.states_url, json=state_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['name'], state_data['name'])

    def test_create_state_invalid_json(self):
        response = self.client.post(
            self.states_url,
            data='invalid_json',
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

    class TestStates(unittest.TestCase):
        """Test cases for the States API."""

        def test_create_state_missing_name(self):
            """Test creating a state with missing name."""
            state_data = {"other_key": "value"}
            response = self.client.post(self.states_url, json=state_data)
            self.assertEqual(response.status_code, 400)
            data = response.get_json()
            self.assertEqual(data['error'], 'Missing name')

    def test_update_state(self):
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            updated_data = {"name": "Updated State"}
            response_update = self.client.put(
                f"{self.states_url}/{state_id}",
                json=updated_data
                )
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertEqual(data_update['name'], updated_data['name'])

    def test_update_nonexistent_state(self):
        updated_data = {"name": "Updated State"}
        response = self.client.put(
            f"{self.states_url}/nonexistent_state_id",
            json=updated_data
            )
        self.assertEqual(response.status_code, 404)

    def test_update_state_invalid_json(self):
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            response = self.client.put(
                f"{self.states_url}/{state_id}",
                data='invalid_json',
                content_type='application/json'
                )
            self.assertEqual(response.status_code, 400)

    def test_update_state_ignore_fields(self):
        # Assuming there is at least one state in the database
        response_all_states = self.client.get(self.states_url)
        data_all_states = response_all_states.get_json()
        if data_all_states:
            state_id = data_all_states[0]['id']
            updated_data = {
                "name": "Updated State",
                "id": "invalid_id",
                "created_at": "invalid_created_at",
                "updated_at": "invalid_updated_at"
                }
            response_update = self.client.put(
                f"{self.states_url}/{state_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertEqual(data_update['name'], updated_data['name'])
            self.assertNotEqual(
                data_update['id'], updated_data['id'])
            self.assertNotEqual(
                data_update['created_at'], updated_data['created_at'])
            self.assertNotEqual(
                data_update['updated_at'], updated_data['updated_at'])
