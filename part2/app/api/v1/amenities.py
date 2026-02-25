from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


def _amenity_payload(a):
    return {"id": a.id, "name": a.name}


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data = request.get_json(silent=True)

        try:
            amenity = facade.create_amenity(data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        return _amenity_payload(amenity), 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()

        if isinstance(amenities, dict):
            amenities = list(amenities.values())

        return [_amenity_payload(a) for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404

        return _amenity_payload(amenity), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        data = request.get_json(silent=True)

        try:
            updated = facade.update_amenity(amenity_id, data)
        except ValueError:
            return {"error": "Invalid input data"}, 400

        if not updated:
            return {"error": "Amenity not found"}, 404

        return {"message": "Amenity updated successfully"}, 200
