from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade
from flask import request

api = Namespace('reviews', description='Review operations')

# Model for creating a review
review_create_model = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for updating a review
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})


def _review_payload(review):
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "place_id": review.place.id,
        "user_id": review.user.id
    }


def _is_admin():
    claims = get_jwt()
    return claims.get("is_admin", False)


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_create_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def post(self):
        """Register a new review"""
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {"error": "Invalid input data"}, 400

        current_user = get_jwt_identity()

        # Never trust user_id from client
        data["user_id"] = current_user

        try:
            review = facade.create_review(data)
        except ValueError as e:
            return {"error": str(e) if str(e) else "Invalid input data"}, 400

        return _review_payload(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [_review_payload(review) for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        return _review_payload(review), 200

    @api.expect(review_update_model, validate=False)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user = get_jwt_identity()
        is_admin = _is_admin()

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {"error": "Invalid input data"}, 400

        # Prevent changing ownership or target place
        data.pop("user_id", None)
        data.pop("place_id", None)

        try:
            updated = facade.update_review(review_id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Review not found"}, 404

        return _review_payload(updated), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        is_admin = _is_admin()

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not is_admin and review.user.id != current_user:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review_id)
        if not deleted:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
