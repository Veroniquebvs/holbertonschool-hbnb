from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# ---- Related models (docs) ----
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# ---- Input model ----
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),

    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


def _place_payload_created(p, owner_id):
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "owner_id": owner_id
    }


def _place_payload_list(p):
    return {
        "id": p.id,
        "title": p.title,
        "latitude": p.latitude,
        "longitude": p.longitude
    }


def _place_payload_detail(p):
    owner = p.owner
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "owner": {
            "id": owner.id,
            "first_name": owner.first_name,
            "last_name": owner.last_name,
            "email": owner.email
        },
        "amenities": [{"id": a.id, "name": a.name} for a in p.amenities],
        "reviews": [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id
            }
            for r in getattr(p, "reviews", [])
        ]
    }


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new place"""
        user_id = get_jwt_identity()
        current_user = facade.get_user(user_id)
        if not current_user:
            return {"error": "User not found"}, 404

        is_admin = current_user.is_admin

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Missing or invalid JSON"}, 400

        if not is_admin:
            data["owner_id"] = user_id

        try:
            place, owner_id = facade.create_place(data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        return _place_payload_created(place, owner_id), 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()
        return [_place_payload_list(p) for p in places], 200


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (including owner, amenities, and reviews)"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return _place_payload_detail(place), 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        user_id = get_jwt_identity()
        current_user = facade.get_user(user_id)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        if not current_user.is_admin and place.owner_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Missing or invalid JSON"}, 400

        try:
            updated = facade.update_place(place_id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Place not found"}, 404

        return {"message": "Place updated successfully"}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
        except ValueError:
            return {"error": "Place not found"}, 404

        return [
            {"id": r.id, "text": r.text, "rating": r.rating}
            for r in (reviews or [])
        ], 200
