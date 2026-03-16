from app import db
from app.models.base_model import BaseModel


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, title, description=None, price=0.0, latitude=0.0,
                 longitude=0.0, owner=None):
        super().__init__()

        if not isinstance(title, str) or not title.strip():
            raise ValueError("title is required and must be a non-empty string")
        if len(title.strip()) > 100:
            raise ValueError("title must be 100 characters or less")

        if description is not None and not isinstance(description, str):
            raise TypeError("description must be a string or None")

        # price: float, positive
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise TypeError("price must be a float")
        if price <= 0:
            raise ValueError("price must be a positive value")

        try:
            latitude = float(latitude)
        except (TypeError, ValueError):
            raise TypeError("latitude must be a float")
        if latitude < -90.0 or latitude > 90.0:
            raise ValueError("latitude must be between -90 and 90")

        try:
            longitude = float(longitude)
        except (TypeError, ValueError):
            raise TypeError("longitude must be a float")
        if longitude < -180.0 or longitude > 180.0:
            raise ValueError("longitude must be between -180 and 180")

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
