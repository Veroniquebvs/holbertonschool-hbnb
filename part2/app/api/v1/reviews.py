from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

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
    def post(self):
        """Register a new review"""
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return {"error": "Invalid input data"}, 400

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
    def put(self, review_id):
        """Update a review's information"""
        data = request.get_json(silent=True)

        try:
            updated = facade.update_review(review_id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Review not found"}, 404

        return _review_payload(updated), 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
        except ValueError:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
