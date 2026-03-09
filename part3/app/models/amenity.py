from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        # name: required, string, max 50
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name is required and must be a non-empty string")

        if len(name) > 50:
            raise ValueError("name must be 50 characters or less")

        self.name = name.strip()
