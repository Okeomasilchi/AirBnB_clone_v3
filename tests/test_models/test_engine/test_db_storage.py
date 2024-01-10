#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def setUp(self):
        """Set up the test environment"""
        self.db_storage = DBStorage()
        self.db_storage.reload()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def tearDown(self):
        """Clean up the test environment"""
        self.db_storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all(self):
        """Test the all method"""
        # Add test objects to the database
        obj1 = State(name="California")
        obj2 = City(name="San Francisco", state_id=obj1.id)
        self.db_storage.new(obj1)
        self.db_storage.new(obj2)
        self.db_storage.save()

        # Retrieve all objects
        all_objs = self.db_storage.all()

        # Check if the objects are retrieved correctly
        self.assertIn("State.{}".format(obj1.id), all_objs)
        self.assertIn("City.{}".format(obj2.id), all_objs)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test the new method"""
        # Create a new object
        obj = State(name="New York")

        # Add the object to the database
        self.db_storage.new(obj)
        self.db_storage.save()

        # Retrieve the object from the database
        retrieved_obj = self.db_storage.get(State, obj.id)

        # Check if the object is retrieved correctly
        self.assertEqual(retrieved_obj, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test the save method"""
        # Create a new object
        obj = State(name="Texas")

        # Add the object to the database
        self.db_storage.new(obj)

        # Save the changes
        self.db_storage.save()

        # Retrieve the object from the database
        retrieved_obj = self.db_storage.get(State, obj.id)

        # Check if the object is retrieved correctly
        self.assertEqual(retrieved_obj, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_delete(self):
        """Test the delete method"""
        # Create a new object
        obj = State(name="Florida")

        # Add the object to the database
        self.db_storage.new(obj)
        self.db_storage.save()

        # Delete the object from the database
        self.db_storage.delete(obj)
        self.db_storage.save()

        # Retrieve the object from the database
        retrieved_obj = self.db_storage.get(State, obj.id)

        # Check if the object is deleted
        self.assertIsNone(retrieved_obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test the get method"""
        # Create a new object
        obj = State(name="Arizona")

        # Add the object to the database
        self.db_storage.new(obj)
        self.db_storage.save()

        # Retrieve the object using the get method
        retrieved_obj = self.db_storage.get(State, obj.id)

        # Check if the object is retrieved correctly
        self.assertEqual(retrieved_obj, obj)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test the count method"""
        # Create multiple objects
        obj1 = State(name="Washington")
        obj2 = State(name="Oregon")
        obj3 = City(name="Seattle", state_id=obj1.id)

        # Add the objects to the database
        self.db_storage.new(obj1)
        self.db_storage.new(obj2)
        self.db_storage.new(obj3)
        self.db_storage.save()

        # Count the number of objects
        count_all = self.db_storage.count()
        count_state = self.db_storage.count(State)
        count_city = self.db_storage.count(City)

        # Check if the counts are correct
        self.assertEqual(
            count_all,
            len(self.db_storage.all())
            )
        self.assertEqual(
            count_state,
            len(self.db_storage.all(State))
            )
        self.assertEqual(
            count_city,
            len(self.db_storage.all(City))
            )
