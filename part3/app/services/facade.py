from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.review import Review

from app.models.place import Place

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
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

    # -------------- Review methods -----------------------

    def _validate_review(self, review_data):
        """Raise ValueError if review_data is invalid"""

        if not isinstance(review_data, dict):
            raise TypeError("review_data must be a dictionary")

        user_id = review_data.get("user_id")
        place_id = review_data.get("place_id")
        text = review_data.get("text")
        rating = review_data.get("rating")

        if not all([user_id, place_id, text, rating]):
            raise ValueError("Missing required fields")

        user = self.user_repo.get(user_id)
        if user is None:
            raise ValueError("User not found")

        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5")

        return text, rating, place, user

    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation
        # for user_id, place_id, and rating
        text, rating, place, user = self._validate_review(review_data)
        review = Review(text, rating, place, user)
        self.review_repo.add(review)
        place.add_review(review)
        return review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        review = self.review_repo.get(review_id)

        return review

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        place = self.place_repo.get(place_id)
        if place is None:
            raise ValueError("Place not found")
        return place.reviews

    def _validate_update_review(self, review_data):
        """ Raise ValueError if update review_data is invalid"""
        if not isinstance(review_data, dict):
            raise TypeError("review_data must be a dictionary")

        if "text" in review_data:
            text = review_data["text"]
            if not isinstance(text, str) or not text.strip():
                raise ValueError("text must be a non-empty string")

        if "rating" in review_data:
            rating = review_data["rating"]
            if not isinstance(rating, int) or rating < 1 or rating > 5:
                raise ValueError("rating must be between 1 and 5")

        return review_data

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        review = self.review_repo.get(review_id)
        if review is None:
            raise ValueError("Review not found")

        update_review = self._validate_update_review(review_data)
        self.review_repo.update(review_id, update_review)
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        place = review.place
        if place and hasattr(place, "reviews"):
            place.reviews = [r for r in place.reviews if r.id != review_id]

        self.review_repo.delete(review_id)
        return True
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

        if title is None or price is None or latitude is None or longitude is None or not owner_id:
            raise ValueError("Invalid input data")

        if not isinstance(amenities_ids, list):
            raise ValueError("Invalid input data")

        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Invalid input data")

        amenities = []
        for aid in amenities_ids:
            a = self.amenity_repo.get(aid)
            if not a:
                raise ValueError("Invalid input data")
            amenities.append(a)

        place = Place(
            title=title,
            description=description,
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        place.amenities = amenities

        self.place_repo.add(place)

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

        if "owner_id" in place_data:
            owner_id = place_data.get("owner_id")
            if not owner_id:
                raise ValueError("Invalid input data")
            owner = self.user_repo.get(owner_id)
            if not owner:
                raise ValueError("Invalid input data")
            place.owner = owner

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

        allowed = {}
        for key in ("title", "description", "price", "latitude", "longitude"):
            if key in place_data:
                allowed[key] = place_data[key]

        self.place_repo.update(place_id, allowed)

        return self.place_repo.get(place_id)
