# Tests by pytest

This document describes the tests performed for the HBnB application, covering the endpoints **Users, Amenities, Places and Reviews**.

## Tools and technologies

- **Python 3.12**
- **Flask** et **Flask-RESTX** pour l'API
- **Pytest** pour les tests unitaires et d'intégration

Tests run from the project root with : **PYTHONPATH=.pytest -v tests**

## Test File Structure

The tests are divided into 4 files, corresponding to the API namespaces:

- `tests/test_users.py`: tests for the `/users/` endpoint

- `tests/test_amenities.py`: tests for the `/amenities/` endpoint

- `tests/test_places.py`: tests for the `/places/` endpoint

- `tests/test_reviews.py`: tests for the `/reviews/` endpoint

## Types of Tests Performed

1. **Creation** (POST)

- Verifies that a new object is created and returns an ID.

- Example: creating a user or a place.

2. **Retrieval** (GET)

- Verifies that the list or individual object is correctly returned.

- Handles 404 errors if the object does not exist.

3. **Update** (PUT)

- Verifies that the object can be updated with new data.

4. **Deletion** (DELETE, for reviews)

- Verifies that the object can be deleted and is no longer accessible.

5. **Error Handling**

- Tests for invalid entries or non-existent objects (returns 400 or 404).

## Results

All Pytest unit tests pass: 12/12.

- The endpoints correctly handle:

- Object creation and retrieval

- Invalid inputs

- Non-existent objects (404)

```
veronique@DESKTOP-2QQLIC1:~/hbnb/holbertonschool-hbnb/part2$ PYTHONPATH=. pytest -v tests
========================================================= test session starts =========================================================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0 -- /home/veronique/hbnb/venv/bin/python3
cachedir: .pytest_cache
rootdir: /home/veronique/hbnb/holbertonschool-hbnb/part2
plugins: flask-1.3.0
collected 12 items                                                                                                                    

tests/test_amenities.py::test_create_amenity PASSED                                                                             [  8%]
tests/test_amenities.py::test_get_amenities PASSED                                                                              [ 16%]
tests/test_amenities.py::test_get_amenity_not_found PASSED                                                                      [ 25%]
tests/test_places.py::test_create_place PASSED                                                                                  [ 33%]
tests/test_places.py::test_get_places PASSED                                                                                    [ 41%]
tests/test_places.py::test_get_place_not_found PASSED                                                                           [ 50%]
tests/test_reviews.py::test_create_review PASSED                                                                                [ 58%]
tests/test_reviews.py::test_get_review_not_found PASSED                                                                         [ 66%]
tests/test_reviews.py::test_update_and_delete_review PASSED                                                                     [ 75%]
tests/test_users.py::test_create_user PASSED                                                                                    [ 83%]
tests/test_users.py::test_get_users PASSED                                                                                      [ 91%]
tests/test_users.py::test_get_user_not_found PASSED                                                                             [100%]

========================================================= 12 passed in 0.52s =========================================================
```