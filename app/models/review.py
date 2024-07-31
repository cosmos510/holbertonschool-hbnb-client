from models.base_model import BaseModel
from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from db import db
import uuid


class Review(BaseModel, db.Model):
    """
    Review class representing reviews of places by users.

    Attributes:
        id (str): Unique identifier for the review, automatically generated
        using UUID.
        user_id (str): ID of the user who created the review, references the
        'users' table.
        place_id (str): ID of the place being reviewed, references the 'places'
        table.
        rating (int): Rating given to the place by the user.
        comment (str, optional): Comment provided by the user about the place.

    Table Name:
        reviews

    Relationships:
        user (User): Relationship to the User model, representing the user who
        created the review.
        place (Place): Relationship to the Place model, representing the place
        being reviewed.

    Methods:
        __init__(self, user_id, place_id, rating, comment=None):
            Initializes a new instance of the Review class.
        to_dict(self):
            Converts the Review object to a dictionary representation.
    """

    __tablename__ = "reviews"

    id = Column(String(256), nullable=False, default=lambda: str(uuid.uuid4()),
                primary_key=True)
    user_id = Column(String(256), ForeignKey("users.id"), nullable=False)
    place_id = Column(String(50), ForeignKey("places.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500))
    uniq_id = Column(String(256), unique=True, nullable=False,
                     default=lambda: str(uuid.uuid4()))

    user = relationship("User", backref="reviews")
    place = relationship("Place", backref="reviews")

    def __init__(self, user_id, place_id, rating, comment):
        """Initialzes the class Review with the following parmeters:
        :param user_id: UUID - Unique ID of an User.
        :param place_id: UUID - Unique ID of a Place.
        :param rating: int - rating given to a Place by an User.
        :param comment: str - comment given to a Place by an User."""
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        """
        Converts the Review object to a dictionary
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": self.rating,
            "comment": self.comment,
        }
