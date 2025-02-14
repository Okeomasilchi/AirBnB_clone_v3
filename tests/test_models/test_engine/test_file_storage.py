#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from json import dumps as js
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def setUp(self):
        """Set up the test environment"""
        self.storage = FileStorage()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def tearDown(self):
        """Clean up the test environment"""
        self.storage.delete()

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """Test that new adds an object to the FileStorage.__objects attr"""
        save = self.storage._FileStorage__objects
        self.storage._FileStorage__objects = {}
        test_dict = {}
        for cls in [Amenity, BaseModel, City, Place, Review, State, User]:
            instance = cls()
            instance_key = instance.__class__.__name__ + "." + instance.id
            self.storage.new(instance)
            test_dict[instance_key] = instance
            self.assertEqual(test_dict, self.storage._FileStorage__objects)
        self.storage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_dict = {}
        for cls in [Amenity, BaseModel, City, Place, Review, State, User]:
            instance = cls()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = self.storage._FileStorage__objects
        self.storage._FileStorage__objects = new_dict
        self.storage.save()
        self.storage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_reload(self):
        """Test that reload properly deserializes the JSON file"""
        with open("file.json", "w") as f:
            f.write(js({"BaseModel.123": {
                        "__class__": "BaseModel",
                        "id": "123"
                        }
                        }))
        self.storage.reload()
        self.assertIn("BaseModel.123", self.storage._FileStorage__objects)
        obj = self.storage._FileStorage__objects["BaseModel.123"]
        self.assertIsInstance(obj, BaseModel)
        self.assertEqual(obj.id, "123")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_delete(self):
        """Test that delete removes an object from __objects"""
        instance = BaseModel()
        instance_key = instance.__class__.__name__ + "." + instance.id
        self.storage.new(instance)
        self.assertIn(instance_key, self.storage._FileStorage__objects)
        self.storage.delete(instance)
        self.assertNotIn(instance_key, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_close(self):
        """Test that close calls reload method"""
        self.assertIsNone(self.storage.close())

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get retrieves an instance by
        class and id"""
        instance = BaseModel()
        instance_key = instance.__class__.__name__ + "." + instance.id
        self.storage.new(instance)
        retrieved_instance = self.storage.get(BaseModel, instance.id)
        self.assertEqual(retrieved_instance, instance)
        self.assertIsNone(self.storage.get(BaseModel, "invalid_id"))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count returns the number of objects"""
        instance = BaseModel()
        self.storage.new(instance)
        self.assertEqual(
            self.storage.count(), len(self.storage.all()))
        self.assertEqual(
            self.storage.count(BaseModel),
            len(self.storage.all(BaseModel))
            )
        self.assertEqual(
            self.storage.count(Amenity),
            len(self.storage.all(Amenity))
            )
