from sqlalchemy import String, Column, Integer
from db import db


class Country(db.Model):
    """
    Defines the Country class representing a country with its name
    and code.

    Attributes:
        id (int): Unique identifier for the country, automatically
        incremented.
        name (str): Name of the country.
        code (str): International code of the country.

    Table Name:
        countries

    Methods:
        __init__(self, name, code):
            Initializes a new instance of the Country class.
        to_dict(self):
            Converts the Country object to a dictionary representation.
    """

    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    code = Column(String(30), nullable=False)

    def __init__(self, name, code):
        """Initializes the class Country wth the following parameters:
        :param name: str - Name of the Country.
        :param code: str - The Country international code."""
        self.name = name
        self.code = code

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code
        }
