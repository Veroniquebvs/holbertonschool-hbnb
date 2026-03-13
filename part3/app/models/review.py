from .base_model import BaseModel
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, text, rating, place_id, user_id):
        super().__init__()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")

        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        if not place_id or not isinstance(place_id, str):
            raise ValueError("place_id is required")

        if not user_id or not isinstance(user_id, str):
            raise ValueError("user_id is required")

        self.text = text.strip()
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
