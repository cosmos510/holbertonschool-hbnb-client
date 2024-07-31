from models.base_model import BaseModel
from sqlalchemy import String, Column, Float, Integer
from db import db
import uuid


class Place(BaseModel, db.Model):
    """
    Place class representing a location available for booking.

    Attributes:
        id (str): Unique identifier for the place, automatically generated
        using UUID.
        name (str): Name of the place.
        description (str): Description of the place.
        address (str): Address of the place.
        city_id (str): ID of the city where the place is located.
        latitude (float): Latitude coordinates of the place.
        longitude (float): Longitude coordinates of the place.
        host_id (str): ID of the host or owner of the place.
        num_rooms (int): Number of rooms in the place.
        num_bathrooms (int): Number of bathrooms in the place.
        price_per_night (float): Price per night for booking the place.
        max_guests (int): Maximum number of guests the place can accommodate.
        amenity_ids (str, optional): IDs of amenities available at the place.

    Table Name:
        places

    Methods:
        __init__(self, name, description, address, city_id, latitude,
        longitude, host_id, num_rooms, num_bathrooms, price_per_night,
        max_guests, amenity_ids=None):

        => Initializes a new instance of the Place class.
    """

    __tablename__ = "places"

    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()),
                primary_key=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    address = Column(String(256), nullable=False)
    city_id = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    host_id = Column(String(256), nullable=False)
    num_rooms = Column(Integer, nullable=False)
    num_bathrooms = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    max_guests = Column(Integer, nullable=False)
    amenity_ids = Column(String(256), nullable=True)
    uniq_id = Column(String(256), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))

    def __init__(self, name, description, address, city_id, latitude,
                 longitude, host_id, num_rooms, num_bathrooms,
                 price_per_night, max_guests, amenity_ids):
        """Initializes the class Place with the following parameters:
        :param name: str - name of the place.
        :param description: star - a description of the place.
        :param address: str - the adress of the place.
        :param city_id: UUID - Unique ID of the City the Place is in.
        :param lattitude: float - the lattitude at wich the Place is.
        :param longitude: float - the longitude at wich the Place is.
        :param host_id: UUID - Unique ID of the owner of the Place.
        :param num_room: int -  number of room the Place is composed of.
        :param num_bathrooms: int - number of bathroom in the Place.
        :param price_per_night: float - price of the Place, per night.
        :param max_guests: int - number of guests the Place can accept.
        """
        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.num_rooms = num_rooms
        self.num_bathrooms = num_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids
