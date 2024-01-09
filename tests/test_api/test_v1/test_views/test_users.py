#!/usr/bin/python3

"""
Models for the routes of the User_views
"""

import json
from flask import Flask
import unittest
from api.v1.app import app


class Test_UserAPI(unittest.TestCase):
    """
    This class contains unit tests for the User API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment before each test case.
        """
        app.config['TESTING'] = True
        self.users_url = "http://0.0.0.0:5000/api/v1/users"
        self.client = app.test_client()

    def tearDown(self):
        """
        Clean up the test environment after each test case.
        """
        app.teardown_appcontext

    def test_get_all_users(self):
        """
        Test case for getting all users.
        """
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_specific_user(self):
        """
        Test case for getting a specific user.
        """
        response_all_users = self.client.get(self.users_url)
        data_all_users = response_all_users.get_json()
        if data_all_users:
            user_id = data_all_users[0]['id']
            response_specific_user = self.client.get(
                f"{self.users_url}/{user_id}")
            self.assertEqual(response_specific_user.status_code, 200)
            data_specific_user = response_specific_user.get_json()
            self.assertIsInstance(data_specific_user, dict)
            self.assertEqual(data_specific_user['id'], user_id)

    def test_get_nonexistent_user(self):
        """
        Test case for getting a nonexistent user.
        """
        response = self.client.get(f"{self.users_url}/nonexistent_user_id")
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_user(self):
        """
        Test case for deleting a nonexistent user.
        """
        response = self.client.delete(f"{self.users_url}/nonexistent_user_id")
        self.assertEqual(response.status_code, 404)

    def test_create_user(self):
        """
        Test case for creating a new user.
        """
        user_data = {"email": "newuser@example.com", "password": "password123"}
        response = self.client.post(self.users_url, json=user_data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsInstance(data, dict)
        self.assertEqual(data['email'], user_data['email'])

    def test_create_user_invalid_json(self):
        """
        Test case for creating a new user with invalid JSON data.
        """
        response = self.client.post(
            self.users_url,
            data='invalid_json',
            content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_email(self):
        """
        Test case for creating a new user with missing email.
        """
        user_data = {"password": "password123"}
        response = self.client.post(self.users_url, json=user_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing email')

    def test_create_user_missing_password(self):
        """
        Test case for creating a new user with missing password.
        """
        user_data = {"email": "newuser@example.com"}
        response = self.client.post(self.users_url, json=user_data)
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Missing password')

    def test_update_user(self):
        """
        Test case for updating an existing user.
        """
        response_all_users = self.client.get(self.users_url)
        data_all_users = response_all_users.get_json()
        if data_all_users:
            user_id = data_all_users[0]['id']
            updated_data = {
                "email": "updateduser@example.com",
                "password": "updatedpassword123"
                }
            response_update = self.client.put(
                f"{self.users_url}/{user_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertNotEqual(data_update['email'], updated_data['email'])

    def test_update_nonexistent_user(self):
        """
        Test case for updating a nonexistent user.
        """
        updated_data = {
            "email": "updateduser@example.com",
            "password": "updatedpassword123"
            }
        response = self.client.put(
            f"{self.users_url}/nonexistent_user_id", json=updated_data)
        self.assertEqual(response.status_code, 404)

    def test_update_user_invalid_json(self):
        """
        Test case for updating a user with invalid JSON data.
        """
        response_all_users = self.client.get(self.users_url)
        data_all_users = response_all_users.get_json()
        if data_all_users:
            user_id = data_all_users[0]['id']
            response = self.client.put(
                f"{self.users_url}/{user_id}",
                data='invalid_json',
                content_type='application/json'
                )
            self.assertEqual(response.status_code, 400)

    def test_update_user_ignore_fields(self):
        """
        Test case for updating a user and ignoring certain fields.
        """
        # Assuming there is at least one user in the database
        response_all_users = self.client.get(self.users_url)
        data_all_users = response_all_users.get_json()
        if data_all_users:
            user_id = data_all_users[0]['id']
            updated_data = {
                "email": "updateduser@example.com",
                "password": "updatedpassword123",
                "id": "invalid_id",
                "created_at": "invalid_created_at",
                "updated_at": "invalid_updated_at"
                }
            response_update = self.client.put(
                f"{self.users_url}/{user_id}", json=updated_data)
            self.assertEqual(response_update.status_code, 200)
            data_update = response_update.get_json()
            self.assertIsInstance(data_update, dict)
            self.assertIn('email', data_update)  # Check if 'email' is present
            self.assertNotEqual(
                data_update['email'], updated_data['email'])
            self.assertNotEqual(
                data_update['id'], updated_data['id'])
            self.assertNotEqual(
                data_update['created_at'], updated_data['created_at'])
            self.assertNotEqual(
                data_update['updated_at'], updated_data['updated_at'])
