import re
from app import db, bcrypt
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship('Place', backref='owner', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')

    def hash_password(self, password):
        """Hashes the password before storing it."""
        if not isinstance(password, str) or not password:
            raise ValueError("password is required")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def update(self, data):
        """Update user fields with validation and secure password hashing."""

        if "first_name" in data:
            first_name = data["first_name"]
            if not isinstance(first_name, str) or not first_name.strip():
                raise ValueError("first_name is required and must be a non-empty string")
            if len(first_name.strip()) > 50:
                raise ValueError("first_name must be 50 characters or less")
            self.first_name = first_name.strip()

        if "last_name" in data:
            last_name = data["last_name"]
            if not isinstance(last_name, str) or not last_name.strip():
                raise ValueError("last_name is required and must be a non-empty string")
            if len(last_name.strip()) > 50:
                raise ValueError("last_name must be 50 characters or less")
            self.last_name = last_name.strip()

        if "email" in data:
            email = data["email"]
            if not isinstance(email, str) or not email.strip():
                raise ValueError("email is required and must be a non-empty string")

            email = email.strip().lower()
            email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
            if not re.match(email_regex, email):
                raise ValueError("email format is invalid")

            self.email = email

        if "password" in data:
            password = data["password"]
            if not isinstance(password, str) or not password:
                raise ValueError("password is required")
            self.hash_password(password)

        if "is_admin" in data:
            is_admin = data["is_admin"]
            if not isinstance(is_admin, bool):
                raise TypeError("is_admin must be a boolean")
            self.is_admin = is_admin
