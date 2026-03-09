from app.models.base_model import BaseModel
from app.models.user import User

class Place(BaseModel):
    def __init__(self, title, description=None, price=0.0, latitude=0.0, longitude=0.0, owner=None):
        super().__init__()

        # title: required, string, max 100
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title is required and must be a non-empty string")
        if len(title) > 100:
            raise ValueError("title must be 100 characters or less")

        # description: optional, string if provided
        if description is not None and not isinstance(description, str):
            raise TypeError("description must be a string or None")

        #price: float, positive
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise TypeError("price must be a float")
        if price <= 0:
            raise ValueError("price must be a positive value")

        # latitude: float in [-90, 90]
        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise TypeError("latitude must be a float")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90 and 90")

        # longitude: float in [ -180, 180]
        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise TypeError("longitude must be a float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180.0 and 180.0")

        # owner: must be a User instance
        if not isinstance(owner, User):
            raise ValueError("owner must be a User instance")

        self.title = title.strip()
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
    
    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
