# HBnB

HBnB is a simplified version of the Airbnb app

## Project structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│       ├── __init__.py
│       ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

## Explanation

This **app**/directory contains the main source code of the application.

The **api**/subdirectory contains the API endpoints, organized by version (v1/).

The **models**/subdirectory contains the business logic classes (for example, user.py, place.py).

The **services**/subdirectory is where the Facade model is implemented, managing the interaction between the layers.

The **persistence**/subdirectory contains the in-memory repository. This will later be replaced by a solution using a database with SQLAlchemy.

**run.py** is the entry point for running the Flask application.

**config.py** will be used to configure environment variables and application settings.

**requirements.txt** will list all the Python packages needed for the project.

**README.md** will contain a brief overview of the project.

**__init__.py** This tells Python to treat these directories as importable packages.


## Business Logic Layer

The business logic layer is composed of four main entities that inherit from a `BaseModel` base class providing a UUID, `created_at` and `updated_at` timestamps for each object.

### Entities

**BaseModel** (`basemodel.py`): Base class inherited by all entities. Provides a unique UUID identifier, creation and modification timestamps, a `save()` method to update `updated_at`, and an `update()` method to modify attributes from a dictionary.

**User** (`user.py`): Represents a user of the application. Contains a first name, last name, email (unique, required) and an `is_admin` boolean (default: `False`).

**Place** (`place.py`): Represents a listing. Contains a title, description, price per night, GPS coordinates (latitude/longitude) and a reference to its owner (a `User`). A place can have multiple reviews and amenities.

**Review** (`review.py`): Represents a review left by a user on a place. Contains the review text, a rating between 1 and 5, and references to the associated `Place` and `User`.

**Amenity** (`amenity.py`): Represents an amenity available at a place (e.g. Wi-Fi, Parking). Contains a name with a maximum length of 50 characters.

### Relationships

- A `User` can own multiple `Place` instances (one-to-many)
- A `Place` can have multiple `Review` instances (one-to-many)
- A `Place` can have multiple `Amenity` instances (many-to-many)

## Class test

### User class test

```
from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.com", password="azerty")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example.com"
    assert user.password == "azerty"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()
```

```
veronique@DESKTOP-2QQLIC1:~/hbnb/holbertonschool-hbnb/part2$ python test_app_models_user.py 
User creation test passed!
```

### Place class test

```
from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.com", password="menton")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194, owner=owner)

    # Adding a review
    review = Review(text="Great stay!", rating=5, place=place, user=owner)
    place.add_review(review)

    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()
```

```
veronique@DESKTOP-2QQLIC1:~/hbnb/holbertonschool-hbnb/part2$ python test_app_place_with_relation.py 
Place creation and relationship test passed!
```

### Amenity class test

```
from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()
```

```
veronique@DESKTOP-2QQLIC1:~/hbnb/holbertonschool-hbnb/part2$ python test_models_amenity.py 
Amenity creation test passed!
```

## Install the dependencies

```
pip install -r requirements.txt
```

`requirements.txt` file caontains:

```
flask
flask-restx
```

## Launch the application

```
python run.py
```

## Architecture

The application is based on three layers that communicate via the **Facade pattern**:

- **Presentation (API)**: receives HTTP requests and returns JSON responses
- **Business Logic (Models + Facade)**: processes data and applies business rules
- **Persistence (Repository)**: stores and retrieves objects (currently in memory, database in part 3)

