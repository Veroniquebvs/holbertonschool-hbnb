from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Model for creating a user
user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(
        required=True,
        description='Email of the user'
    ),
    'password': fields.String(
        required=True,
        description='Password of the user'
    )
})

# Model for normal user update
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user')
})

# Model for admin update
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status')
})


def _user_payload(user):
    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }


def _is_admin():
    claims = get_jwt()
    return claims.get("is_admin", False)


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user (admin only)"""
        if not _is_admin():
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if not isinstance(user_data, dict):
            return {'error': 'Invalid input data'}, 400

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return _user_payload(new_user), 201

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [_user_payload(user) for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return _user_payload(user), 200

    @api.expect(admin_user_update_model, validate=False)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Missing or invalid token')
    @jwt_required()
    def put(self, user_id):
        """Update a user"""
        current_user_id = get_jwt_identity()
        is_admin = _is_admin()

        user_data = api.payload
        if not isinstance(user_data, dict):
            return {'error': 'Invalid input data'}, 400

        # Non-admin can only modify their own profile
        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized action'}, 403

        # Non-admin cannot modify email or password
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password.'}, 400

        # If email is being changed, ensure uniqueness
        email = user_data.get('email')
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        updated_user = facade.update_user(user_id, user_data, is_admin=is_admin)

        if not updated_user:
            return {'error': 'User not found'}, 404

        return _user_payload(updated_user), 200