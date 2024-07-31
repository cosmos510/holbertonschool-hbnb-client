from models.base_model import BaseModel
from db import db
from sqlalchemy import String, Integer, Column, ForeignKey
import uuid


class City(BaseModel, db.Model):
    """
    Represents a city with its name and the country it belongs to.

    Attributes:
        id (str): Unique identifier for the city, generated automatically.
        name (str): Name of the city.
        country_id (str): ID of the country to which the city belongs.
        uniq_id (str): Unique identifier for the city, generated automatically.

    Table Name:
        cities

    Methods:
        __init__(self, name, country_id):
            Initializes a new instance of the City class.
        to_dict(self):
            Converts the City object to a dictionary representation.
    """

    __tablename__ = "cities"
    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()),
                primary_key=True)
    name = Column(String(128), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    uniq_id = Column(String(60), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))

    def __init__(self, name, country_id):
        """
        Initializes a new instance of the City class.

        Args:
            name (str): Name of the city.
            country_id (str): ID of the country to which the city belongs.
        """
        super().__init__()
        self.name = name
        self.country_id = country_id

    def to_dict(self):
        """
        Converts the City object to a dictionary representation.

        Returns:
            dict: Dictionary containing the name, country_id, and uniq_id of
            the city.
        """
        return {
            "name": self.name,
            "country_id": self.country_id,
            "uniq_id": self.uniq_id
        }
