from app.models.base_model import BaseModel
from app.models.place import Place
from app.models.user import User


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        # text: required, string
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required and must be a non-empty string")

        # rating: integer between 1 and 5
        if not isinstance(rating, int):
            raise TypeError("rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

        # place: must be a Place instance
        if not isinstance(place, Place):
            raise ValueError("place must be a Place instance")

        # user: must be a User instance
        if not isinstance(user, User):
            raise ValueError("user must be a User instance")

        self.text = text.strip()
        self.rating = rating
        self.place = place
        self.user = user
