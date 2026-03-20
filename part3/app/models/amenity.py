from app import db
from .base_model import BaseModel


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        super().__init__()

        if not isinstance(name, str) or not name.strip():
            raise ValueError("name is required and must be a non-empty string")

        name = name.strip()
        if len(name) > 50:
            raise ValueError("name must be 50 characters or less")

        self.name = name
