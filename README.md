# AirBnB Clone - The Console

The console is the first segment of the AirBnB project at Holberton School that will collectively cover fundamental concepts of higher level programming. The goal of AirBnB project is to eventually deploy our server a simple copy of the AirBnB Website(HBnB). A command interpreter is created in this segment to manage objects for the AirBnB(HBnB) website.

#### Functionalities of this command interpreter:

- Create a new object (ex: a new User or a new Place)
- Retrieve an object from a file, a database etc...
- Do operations on objects (count, compute stats, etc...)
- Update attributes of an object
- Destroy an object

## Table of Content

- [Environment](#environment)
- [Installation](#installation)
- [File Descriptions](#file-descriptions)
- [Usage](#usage)
- [Examples of use](#examples-of-use)
- [Bugs](#bugs)
- [Api](#api)
- [Authors](#authors)
- [License](#license)

## Environment

This project is interpreted/tested on Ubuntu 14.04 LTS using python3 (version 3.4.3)

## Installation

- Clone this repository: `git clone "https://github.com/alexaorrico/AirBnB_clone.git"`
- Access AirBnb directory: `cd AirBnB_clone`
- Run hbnb(interactively): `./console` and enter command
- Run hbnb(non-interactively): `echo "<command>" | ./console.py`

## File Descriptions

[console.py](console.py) - the console contains the entry point of the command interpreter.
List of commands this console current supports:

- `EOF` - exits console
- `quit` - exits console
- `<emptyline>` - overwrites default emptyline method and does nothing
- `create` - Creates a new instance of`BaseModel`, saves it (to the JSON file) and prints the id
- `destroy` - Deletes an instance based on the class name and id (save the change into the JSON file).
- `show` - Prints the string representation of an instance based on the class name and id.
- `all` - Prints all string representation of all instances based or not on the class name.
- `update` - Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file).

#### `models/` directory contains classes used for this project:

[base_model.py](/models/base_model.py) - The BaseModel class from which future classes will be derived

- `def __init__(self, *args, **kwargs)` - Initialization of the base model
- `def __str__(self)` - String representation of the BaseModel class
- `def save(self)` - Updates the attribute `updated_at` with the current datetime
- `def to_dict(self)` - returns a dictionary containing all keys/values of the instance

Classes inherited from Base Model:

- [amenity.py](/models/amenity.py)
- [city.py](/models/city.py)
- [place.py](/models/place.py)
- [review.py](/models/review.py)
- [state.py](/models/state.py)
- [user.py](/models/user.py)

#### `/models/engine` directory contains File Storage class that handles JASON serialization and deserialization :

[file_storage.py](/models/engine/file_storage.py) - serializes instances to a JSON file & deserializes back to instances

- `def all(self)` - returns the dictionary \_\_objects
- `def new(self, obj)` - sets in \_\_objects the obj with key <obj class name>.id
- `def save(self)` - serializes **objects to the JSON file (path: **file_path)
- ` def reload(self)` - deserializes the JSON file to \_\_objects

#### `/tests` directory contains all unit test cases for this project:

[/test_models/test_base_model.py](/tests/test_models/test_base_model.py) - Contains the TestBaseModel and TestBaseModelDocs classes
TestBaseModelDocs class:

- `def setUpClass(cls)`- Set up for the doc tests
- `def test_pep8_conformance_base_model(self)` - Test that models/base_model.py conforms to PEP8
- `def test_pep8_conformance_test_base_model(self)` - Test that tests/test_models/test_base_model.py conforms to PEP8
- `def test_bm_module_docstring(self)` - Test for the base_model.py module docstring
- `def test_bm_class_docstring(self)` - Test for the BaseModel class docstring
- `def test_bm_func_docstrings(self)` - Test for the presence of docstrings in BaseModel methods

TestBaseModel class:

- `def test_is_base_model(self)` - Test that the instatiation of a BaseModel works
- `def test_created_at_instantiation(self)` - Test created_at is a pub. instance attribute of type datetime
- `def test_updated_at_instantiation(self)` - Test updated_at is a pub. instance attribute of type datetime
- `def test_diff_datetime_objs(self)` - Test that two BaseModel instances have different datetime objects

[/test_models/test_amenity.py](/tests/test_models/test_amenity.py) - Contains the TestAmenityDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_amenity(self)` - Test that models/amenity.py conforms to PEP8
- `def test_pep8_conformance_test_amenity(self)` - Test that tests/test_models/test_amenity.py conforms to PEP8
- `def test_amenity_module_docstring(self)` - Test for the amenity.py module docstring
- `def test_amenity_class_docstring(self)` - Test for the Amenity class docstring

[/test_models/test_city.py](/tests/test_models/test_city.py) - Contains the TestCityDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_city(self)` - Test that models/city.py conforms to PEP8
- `def test_pep8_conformance_test_city(self)` - Test that tests/test_models/test_city.py conforms to PEP8
- `def test_city_module_docstring(self)` - Test for the city.py module docstring
- `def test_city_class_docstring(self)` - Test for the City class docstring

[/test_models/test_file_storage.py](/tests/test_models/test_file_storage.py) - Contains the TestFileStorageDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_file_storage(self)` - Test that models/file_storage.py conforms to PEP8
- `def test_pep8_conformance_test_file_storage(self)` - Test that tests/test_models/test_file_storage.py conforms to PEP8
- `def test_file_storage_module_docstring(self)` - Test for the file_storage.py module docstring
- `def test_file_storage_class_docstring(self)` - Test for the FileStorage class docstring

[/test_models/test_place.py](/tests/test_models/test_place.py) - Contains the TestPlaceDoc class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_place(self)` - Test that models/place.py conforms to PEP8.
- `def test_pep8_conformance_test_place(self)` - Test that tests/test_models/test_place.py conforms to PEP8.
- `def test_place_module_docstring(self)` - Test for the place.py module docstring
- `def test_place_class_docstring(self)` - Test for the Place class docstring

[/test_models/test_review.py](/tests/test_models/test_review.py) - Contains the TestReviewDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_review(self)` - Test that models/review.py conforms to PEP8
- `def test_pep8_conformance_test_review(self)` - Test that tests/test_models/test_review.py conforms to PEP8
- `def test_review_module_docstring(self)` - Test for the review.py module docstring
- `def test_review_class_docstring(self)` - Test for the Review class docstring

[/test_models/state.py](/tests/test_models/test_state.py) - Contains the TestStateDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_state(self)` - Test that models/state.py conforms to PEP8
- `def test_pep8_conformance_test_state(self)` - Test that tests/test_models/test_state.py conforms to PEP8
- `def test_state_module_docstring(self)` - Test for the state.py module docstring
- `def test_state_class_docstring(self)` - Test for the State class docstring

[/test_models/user.py](/tests/test_models/test_user.py) - Contains the TestUserDocs class:

- `def setUpClass(cls)` - Set up for the doc tests
- `def test_pep8_conformance_user(self)` - Test that models/user.py conforms to PEP8
- `def test_pep8_conformance_test_user(self)` - Test that tests/test_models/test_user.py conforms to PEP8
- `def test_user_module_docstring(self)` - Test for the user.py module docstring
- `def test_user_class_docstring(self)` - Test for the User class docstring

## Examples of use

```
vagrantAirBnB_clone$./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) all MyModel
** class doesn't exist **
(hbnb) create BaseModel
7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) all BaseModel
[[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}]
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
[BaseModel] (7da56403-cc45-4f1c-ad32-bfafeb2bb050) {'updated_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772167), 'id': '7da56403-cc45-4f1c-ad32-bfafeb2bb050', 'created_at': datetime.datetime(2017, 9, 28, 9, 50, 46, 772123)}
(hbnb) destroy BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
(hbnb) show BaseModel 7da56403-cc45-4f1c-ad32-bfafeb2bb050
** no instance found **
(hbnb) quit
```

## Bugs

No known bugs at this time.

## Api

The project structure is organized as follows:

    api: Contains the API implementation with versioned views.
        v1: Version 1 of the API.
            app.py: Flask application setup and configuration.
            views: Module containing different views for objects like States, Cities, etc.
            states.py: View for State objects.
            cities.py: View for City objects.
            amenities.py: View for Amenity objects.
            users.py: View for User objects.
    models: Contains the data models for the application.

### API Status

The API status endpoint returns a JSON response indicating the status of the API.

Example

```bash
curl -X GET http://0.0.0.0:5000/api/v1/status
```

output

```json
{
  "status": "OK"
}
```

### Statistics Endpoint

The statistics endpoint provides the number of objects for each type.

Example

```bash
GET http://0.0.0.0:5000/api/v1/stats
```

```json
{
  "states": 5,
  "cities": 20,
  "amenities": 10,
  "users": 15
}
```

### Not Found Handling

When a resource is not found, the API returns a JSON-formatted 404 status code response.

**Example**:

```bash
Copy code
GET http://0.0.0.0:5000/api/v1/nop
```

```json
{
  "error": "Not found"
}
```

### State Endpoint

The State endpoint handles all default RESTful API actions for State objects.

```bash
# Retrieve all states
curl -X GET http://0.0.0.0:5000/api/v1/states

# Retrieve a specific state
curl -X GET http://0.0.0.0:5000/api/v1/states/<state_id>

# Delete a state
curl -X DELETE http://0.0.0.0:5000/api/v1/states/<state_id>

# Create a new state
curl -X POST -H "Content-Type: application/json" -d '{"name": "New York"}' http://0.0.0.0:5000/api/v1/states

# Update a state
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated State"}' http://0.0.0.0:5000/api/v1/states/<state_id>
```

Expected JSON Response

```json
{
  "id": "<state_id>",
  "created_at": "2022-01-07T12:34:56.789",
  "updated_at": "2022-01-07T12:34:56.789",
  "name": "New York"
}
```

### City Endpoint

The City endpoint handles all default RESTful API actions for City objects.

Examples

```bash
# Retrieve all cities of a state
curl -X GET http://0.0.0.0:5000/api/v1/states/1/cities

# Retrieve a specific city
curl -X GET http://0.0.0.0:5000/api/v1/cities/<city_id>

# Delete a city
curl -X DELETE http://0.0.0.0:5000/api/v1/cities/<city_id>

# Create a new city
curl -X POST -H "Content-Type: application/json" -d '{"name": "New City"}' http://0.0.0.0:5000/api/v1/states/<state_id>/cities

# Update a city
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated City"}' http://0.0.0.0:5000/api/v1/cities/<city_id>
```

Expected JSON Response

```json
Copy code
{
  "id": "<city_id>",
  "created_at": "2022-01-07T12:34:56.789",
  "updated_at": "2022-01-07T12:34:56.789",
  "name": "New City",
  "state_id": "<state_id>"
}
```

### Amenity Endpoint

The Amenity endpoint handles all default RESTful API actions for Amenity objects.

```bash
# Retrieve all amenities
curl -X GET http://0.0.0.0:5000/api/v1/amenities

# Retrieve a specific amenity
curl -X GET http://0.0.0.0:5000/api/v1/amenities/<amenity_id>

# Delete an amenity
curl -X DELETE http://0.0.0.0:5000/api/v1/amenities/<amenity_id>

# Create a new amenity
curl -X POST -H "Content-Type: application/json" -d '{"name": "Swimming Pool"}' http://0.0.0.0:5000/api/v1/amenities

# Update an amenity
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Updated Amenity"}' http://0.0.0.0:5000/api/v1/amenities/<amenity_id>
```

Expected JSON Response

```json
Copy code
{
  "id": "<amenity_id>",
  "created_at": "2022-01-07T12:34:56.789",
  "updated_at": "2022-01-07T12:34:56.789",
  "name": "Swimming Pool"
}
```

### User Endpoint

The User endpoint handles all default RESTful API actions for User objects.

Examples

```bash
# Retrieve all users
curl -X GET http://0.0.0.0:5000/api/v1/users

# Retrieve a specific user
curl -X GET http://0.0.0.0:5000/api/v1/users/<user_id>

# Delete a user
curl -X DELETE http://0.0.0.0:5000/api/v1/users/<user_id>

# Create a new user
curl -X POST -H "Content-Type: application/json" -d '{"username": "new_user"}' http://0.0.0.0:5000/api/v1/users

# Update a user
curl -X PUT -H "Content-Type: application/json" -d '{"username": "updated_user"}' http://0.0.0.0:5000/api/v1/users/<user_id>
```

Expected JSON Response

```json
Copy code
{
  "id": "<user_id>",
  "created_at": "2022-01-07T12:34:56.789",
  "updated_at": "2022-01-07T12:34:56.789",
  "username": "new_user"
}
```

## Authors

Alexa Orrico - [Github](https://github.com/alexaorrico) / [Twitter](https://twitter.com/alexa_orrico)  
Jennifer Huang - [Github](https://github.com/jhuang10123) / [Twitter](https://twitter.com/earthtojhuang)  
Khadijat Rasaq - [Github](https://github.com/KayDjay) / [Twitter](https://twitter.com/khadijat_rasaq)
Okeomasilachi Onyedibia- [Github](https://github.com/okeomasilchi) / [Twitter](https://twitter.com/okeomasilachi1)

Second part of Airbnb: Joann Vuong

## License

Public Domain. No copy write protection.
