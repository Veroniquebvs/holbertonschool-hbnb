import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()

        # first_name: required, string, max 50
        if not isinstance(first_name, str) or not first_name.strip():
            raise ValueError("first_name is required and must be a non-empty string")
        if len(first_name) > 50:
            raise ValueError("first_name must be 50 characters or less")

        # last_name: required, string, max 50
        if not isinstance(last_name, str) or not last_name.strip():
            raise ValueError("last_name is required and must be a non-empty string")
        if len(last_name) > 50:
            raise ValueError("last_name must be 50 characters or less")

        # email: required, valid format
        if not isinstance(email, str) or not email.strip():
            raise ValueError("email is required and must be a non-empty string")

        email = email.strip().lower()

        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(email_regex, email):
            raise ValueError("email format is invalid")

        # password: required
        if not isinstance(password, str) or not password:
            raise ValueError("password is required")

        # is_admin: boolean
        if not isinstance(is_admin, bool):
            raise TypeError("is_admin must be a boolean")

        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []

    def add_place(self, place):
        """Add a place to the user's list of places."""
        if place not in self.places:
            self.places.append(place)
