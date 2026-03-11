from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, 
                             description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


def _review_payload(review):
    return {
        "id": review.id,
        "text": review.text,
        "rating": review.rating,
        "place_id": review.place.id,
        "user_id": review.user.id
    }


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """Register a new review"""
        user_id = get_jwt_identity()
        current_user = facade.get_user(user_id)
        if not current_user:
            return {"error": "User not found"}, 404

        is_admin = current_user.is_admin

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Review doesn't exists"}, 400

        place_id = data.get("place_id")
        if not place_id:
            return {"error": "Missing place_id"}, 400

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if not is_admin:
            data["user_id"] = user_id

        try:
            review = facade.create_review(data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        return _review_payload(review), 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        result = []
        for i in reviews:
            result.append({
                "id": i.id,
                "text": i.text,
                "rating": i.rating,
                "place_id": i.place.id,
                "user_id": i.user.id
            })
        return result, 200


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

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        user_id = get_jwt_identity()
        current_user = facade.get_user(user_id)

        new_review = facade.get_review(review_id)
        if not new_review:
            return {"error": "Review not found"}, 404
        if not current_user.is_admin and new_review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        data = request.get_json()
        if not data or not isinstance(data, dict):
            return {"error": "Missing or invalid JSON"}, 400

        try:
            updated = facade.update_review(new_review.id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Review not found"}, 404

        return _review_payload(updated), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        user_id = get_jwt_identity()
        current_user = facade.get_user(user_id)
        if not current_user:
            return {"error": "User not found"}, 404

        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        if not current_user.is_admin and review.user_id != user_id:
            return {"error": "Unauthorized action"}, 403

        deleted = facade.delete_review(review.id)
        if not deleted:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
