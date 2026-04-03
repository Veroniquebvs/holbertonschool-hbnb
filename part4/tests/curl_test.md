# cURL API Testing

This document describes manual cURL testing

## User

### Create a user

**Command:**
```
curl -X POST http://127.0.0.1:5000/api/v1/users/ \
-H "Content-Type: application/json" \
-d '{"first_name":"John","last_name":"Doe","email":"john@email.com","password":"1234"}'
```

**Result:**

User successfully created with ID :
```
{
    "id": "875bd553-d382-4bac-87e3-a933a7fb7df8",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@email.com"
}
```
### Get all users

**Command:**
```
curl http://127.0.0.1:5000/api/v1/users/
```

**Result:**

List of users returned :
```
[
    {
        "id": "875bd553-d382-4bac-87e3-a933a7fb7df8",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@email.com"
    }
]
```
### Get user by id

**Command:**
```
curl http://127.0.0.1:5000/api/v1/users/875bd553-d382-4bac-87e3-a933a7fb7df8
```

**Result:**

List of all users returned :
```
{
    "id": "875bd553-d382-4bac-87e3-a933a7fb7df8",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@email.com"
}
```
### Invalid User

**Command:**
```
curl http://127.0.0.1:5000/api/v1/users/invalid
```
**Result:**

Error 404 returned :
```
{
    "error": "User not found"
}
```
## Amenity

### Create Amenity

**Command:**
```
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"WiFi"}'
```
**Result:**

Amenity created successfully:
```
{
    "id": "1c36fd5b-0217-4287-a29d-707a3545824b",
    "name": "WiFi"
}
```
### Get all amenities:

**Command:**
```
curl http://127.0.0.1:5000/api/v1/amenities/
```
**Result:**

List of all amenities returned :
```
[
    {
        "id": "1c36fd5b-0217-4287-a29d-707a3545824b",
        "name": "WiFi"
    }
]
```
## Place

### Create a place:

**Command:**
```
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
"title": "My place",
"description": "Nice place",
"price": 100,
"latitude": 48.85,
"longitude": 2.35,
"owner_id": "875bd553-d382-4bac-87e3-a933a7fb7df8",
"amenities": ["1c36fd5b-0217-4287-a29d-707a3545824b"]
}'
```
**Result:**
The place successfully created :
```
{
    "id": "2f7aebdb-c609-49c3-b0ce-ca503dfd8c24",
    "title": "My place",
    "description": "Nice place",
    "price": 100.0,
    "latitude": 48.85,
    "longitude": 2.35,
    "owner_id": "875bd553-d382-4bac-87e3-a933a7fb7df8"
}
```
## Review:

### Create a review:

**Command:**
```
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
"text": "Great place",
"rating": 5,
"user_id": "875bd553-d382-4bac-87e3-a933a7fb7df8",
"place_id": "b75d3d23-1238-43b0-a084-a82149d7bdcb"
}'
```
**Result:**

Review successfully created :
```
{
    "id": "d945a2a4-3727-43bf-a3b4-c1df5648a1ed",
    "text": "Great place",
    "rating": 5,
    "place_id": "b75d3d23-1238-43b0-a084-a82149d7bdcb",
    "user_id": "875bd553-d382-4bac-87e3-a933a7fb7df8"
}
```
### Delete a review:

**Command:**
```
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/d945a2a4-3727-43bf-a3b4-c1df5648a1ed
```
**Result:**
```
{
    "message": "Review deleted successfully"
}
```
