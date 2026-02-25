from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()

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
    # -------- PLACE METHODS (Task Place) --------

    def create_place(self, place_data):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid input data")

        title = place_data.get("title")
        description = place_data.get("description", None)
        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")
        owner_id = place_data.get("owner_id")
        amenities_ids = place_data.get("amenities", [])

        # Basic required fields check (simple)
        if title is None or price is None or latitude is None or longitude is None or not owner_id:
            raise ValueError("Invalid input data")

        if not isinstance(amenities_ids, list):
            raise ValueError("Invalid input data")

        # Owner must exist
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid input data")

        # Amenities must exist
        amenities = []
        for aid in amenities_ids:
            a = self.amenity_repo.get(aid)
            if not a:
                raise ValueError("Invalid input data")
            amenities.append(a)

        # Create Place (Place model will validate too)
        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        # Attach amenities (many-to-many simplified)
        place.amenities = amenities

        self.place_repo.add(place)

        # On renvoie aussi owner_id pour la réponse POST
        return place, owner_id

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid input data")

        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Handle owner_id update (if present)
        if "owner_id" in place_data:
            owner_id = place_data.get("owner_id")
            if not owner_id:
                raise ValueError("Invalid input data")
            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError("Invalid input data")
            place.owner = owner

        # Handle amenities update (if present)
        if "amenities" in place_data:
            amenities_ids = place_data.get("amenities")
            if not isinstance(amenities_ids, list):
                raise ValueError("Invalid input data")
            amenities = []
            for aid in amenities_ids:
                a = self.amenity_repo.get(aid)
                if not a:
                    raise ValueError("Invalid input data")
                amenities.append(a)
            place.amenities = amenities

        # Update basic fields (if present)
        allowed = {}
        for key in ("title", "description", "price", "latitude", "longitude"):
            if key in place_data:
                allowed[key] = place_data[key]

        # Use BaseModel.update() via repository update
        # (repo.update -> obj.update -> save())
        self.place_repo.update(place_id, allowed)

        return self.place_repo.get(place_id)
