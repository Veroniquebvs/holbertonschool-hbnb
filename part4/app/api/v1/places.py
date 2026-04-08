from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

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

# ---- Input model for create/update ----
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'image_url': fields.String(description='URL of the place image'),
    'amenities': fields.List(
        fields.String,
        required=False,
        description="List of amenities IDs"
    )
})


def _place_payload_created(p):
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "owner_id": p.owner.id
    }


def _place_payload_list(p):
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "image_url": p.image_url
    }


def _place_payload_detail(p):
    owner = p.owner
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "latitude": p.latitude,
        "longitude": p.longitude,
        "image_url": p.image_url,
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
                "user_id": r.user.id,
                "user_name": r.user.first_name
            }
            for r in getattr(p, "reviews", [])
        ]
    }


def _is_admin():
    claims = get_jwt()
    return claims.get("is_admin", False)


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def post(self):
        """Register a new place"""
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt_identity()

        # Force owner_id from JWT
        data["owner_id"] = current_user

        try:
            place = facade.create_place(data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        return _place_payload_created(place), 201

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

    @api.expect(place_input_model, validate=False)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information"""
        current_user = get_jwt_identity()
        is_admin = _is_admin()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin and place.owner.id != current_user:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {"error": "Invalid input data"}, 400

        # Prevent changing ownership from request body
        data.pop("owner_id", None)

        try:
            updated = facade.update_place(place_id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Place not found"}, 404

        return _place_payload_detail(updated), 200


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
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
            }
            for r in (reviews or [])
        ], 200
