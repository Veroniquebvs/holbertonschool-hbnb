from .base_model import BaseModel
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, text, rating):
        super().__init__()

        # text: required, string
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")

        # rating: integer between 1 and 5
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        self.text = text.strip()
        self.rating = rating
