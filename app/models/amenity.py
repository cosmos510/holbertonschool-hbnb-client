from models.base_model import BaseModel
from sqlalchemy import String, Column
from db import db
import uuid


class Amenity(BaseModel, db.Model):
    """
    Represents an Amenity with its name attribute.

    Attributes:
        id (str): Unique identifier for the Amenity instance, generated
        automatically.
        name (str): Name of the Amenity.

    Methods:
        __init__(self, name):
            Initializes a new instance of Amenity.
        to_dict(self):
            Converts the Amenity instance to a dictionary representation.

    Notes:
        This class inherits from BaseModel and is mapped to the "amenities"
        table in the database.
    """

    __tablename__ = "amenities"

    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()),
                primary_key=True)
    name = Column(String(128), nullable=False)
    uniq_id = Column(String(256), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))

    def __init__(self, name):
        """
        Initializes a new instance of Amenity.

        Args:
            name (str): Name of the Amenity.
        """
        super().__init__()
        self.name = name
