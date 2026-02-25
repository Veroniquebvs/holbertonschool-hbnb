from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return self.user_repo.get(user_id)
    # -------- AMENITY METHODS (Task 03) --------

    def _validate_amenity_data(self, amenity_data):
        """Raise ValueError if invalid."""
        if not isinstance(amenity_data, dict):
            raise ValueError("Invalid input data")

        name = amenity_data.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid input data")

        return name.strip()

    def create_amenity(self, amenity_data):
        name = self._validate_amenity_data(amenity_data)

        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        name = self._validate_amenity_data(amenity_data)
        amenity.name = name

        self.amenity_repo.update(amenity_id, {"name": name})
        return amenity
