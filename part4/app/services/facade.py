from app.persistence.repository import SQLAlchemyRepository
from app.services.repositories.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)

    def create_user(self, user_data):
        if not isinstance(user_data, dict):
            raise ValueError("Invalid input data")

        email = user_data.get("email")
        if email and self.user_repo.get_user_by_email(email.strip().lower()):
            raise ValueError("Email already registered")

        password = user_data.pop("password", None)
        if not password:
            raise ValueError("Password is required")

        user = User(**user_data)
        user.hash_password(password)

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        if not isinstance(email, str):
            return None
        return self.user_repo.get_user_by_email(email.strip().lower())

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data, is_admin=False):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if not isinstance(user_data, dict):
            raise ValueError("Invalid input data")

        if not is_admin:
            forbidden_fields = {"email", "password", "id", "is_admin"}
            cleaned_data = {
                key: value for key, value in user_data.items()
                if key not in forbidden_fields
            }
        else:
            cleaned_data = {
                key: value for key, value in user_data.items()
                if key != "id"
            }

        user.update(cleaned_data)
        self.user_repo.update(user_id, cleaned_data)
        return self.user_repo.get(user_id)

    # -------- AMENITY METHODS --------

    def _validate_amenity_data(self, amenity_data):
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

    # -------------- REVIEW METHODS -----------------------

    def _validate_review_data(self, review_data):
        if not isinstance(review_data, dict):
            raise ValueError("Invalid input data")

        validated = {}

        if "text" in review_data:
            text = review_data.get("text")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Invalid input data")
            validated["text"] = text.strip()

        if "rating" in review_data:
            rating = review_data.get("rating")
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("Invalid input data")
            validated["rating"] = rating

        if "place_id" in review_data:
            place_id = review_data.get("place_id")
            if not isinstance(place_id, str) or not place_id.strip():
                raise ValueError("Invalid input data")
            validated["place_id"] = place_id.strip()

        if "user_id" in review_data:
            user_id = review_data.get("user_id")
            if not isinstance(user_id, str) or not user_id.strip():
                raise ValueError("Invalid input data")
            validated["user_id"] = user_id.strip()

        return validated

    def create_review(self, review_data):
        validated = self._validate_review_data(review_data)

        required_fields = {"text", "rating", "place_id", "user_id"}
        if not required_fields.issubset(validated.keys()):
            raise ValueError("Invalid input data")

        user = self.user_repo.get(validated["user_id"])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(validated["place_id"])
        if not place:
            raise ValueError("Place not found")

        if place.owner_id == user.id:
            raise ValueError("You cannot review your own place.")

        existing_review = Review.query.filter_by(
            user_id=user.id,
            place_id=place.id
        ).first()
        if existing_review:
            raise ValueError("You have already reviewed this place.")

        review = Review(
            text=validated["text"],
            rating=validated["rating"],
            place_id=validated["place_id"],
            user_id=validated["user_id"]
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        validated = self._validate_review_data(review_data)
        validated.pop("place_id", None)
        validated.pop("user_id", None)

        if not validated:
            raise ValueError("Invalid input data")

        self.review_repo.update(review_id, validated)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        self.review_repo.delete(review_id)
        return True

    # -------- PLACE METHODS --------

    def _validate_place_data(self, place_data):
        if not isinstance(place_data, dict):
            raise ValueError("Invalid input data")

        validated = {}

        if "title" in place_data:
            title = place_data.get("title")
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Invalid input data")
            if len(title.strip()) > 100:
                raise ValueError("Invalid input data")
            validated["title"] = title.strip()

        if "description" in place_data:
            description = place_data.get("description")
            if description is not None and not isinstance(description, str):
                raise ValueError("Invalid input data")
            validated["description"] = description

        if "price" in place_data:
            try:
                price = float(place_data.get("price"))
            except (TypeError, ValueError):
                raise ValueError("Invalid input data")
            if price <= 0:
                raise ValueError("Invalid input data")
            validated["price"] = price

        if "latitude" in place_data:
            try:
                latitude = float(place_data.get("latitude"))
            except (TypeError, ValueError):
                raise ValueError("Invalid input data")
            if latitude < -90.0 or latitude > 90.0:
                raise ValueError("Invalid input data")
            validated["latitude"] = latitude

        if "longitude" in place_data:
            try:
                longitude = float(place_data.get("longitude"))
            except (TypeError, ValueError):
                raise ValueError("Invalid input data")
            if longitude < -180.0 or longitude > 180.0:
                raise ValueError("Invalid input data")
            validated["longitude"] = longitude

        if "owner_id" in place_data:
            owner_id = place_data.get("owner_id")
            if not isinstance(owner_id, str) or not owner_id.strip():
                raise ValueError("Invalid input data")
            validated["owner_id"] = owner_id.strip()

        if "amenities" in place_data:
            amenities = place_data.get("amenities")
            if not isinstance(amenities, list):
                raise ValueError("Invalid input data")
            validated["amenities"] = amenities

        if "image_url" in place_data:
            image_url = place_data.get("image_url")
            if image_url is not None and not isinstance(image_url, str):
                raise ValueError("Invalid input data")
            validated["image_url"] = image_url

        return validated

    def create_place(self, place_data):
        validated = self._validate_place_data(place_data)

        required_fields = {"title", "price", "latitude", "longitude", "owner_id"}
        if not required_fields.issubset(validated.keys()):
            raise ValueError("Invalid input data")

        owner = self.user_repo.get(validated["owner_id"])
        if not owner:
            raise ValueError("User not found")

        amenities = []
        for amenity_id in validated.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Amenity not found")
            amenities.append(amenity)

        place = Place(
            title=validated["title"],
            description=validated.get("description"),
            price=validated["price"],
            latitude=validated["latitude"],
            longitude=validated["longitude"],
            owner_id=validated["owner_id"],
            image_url=validated.get("image_url")
        )

        place.amenities = amenities

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        validated = self._validate_place_data(place_data)
        validated.pop("owner_id", None)

        if "amenities" in validated:
            amenities = []
            for amenity_id in validated["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Amenity not found")
                amenities.append(amenity)
            place.amenities = amenities
            validated.pop("amenities")

        if not validated and "amenities" not in place_data:
            raise ValueError("Invalid input data")

        self.place_repo.update(place_id, validated)
        return self.place_repo.get(place_id)
