import uuid
import datetime
from flask import jsonify
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime
from db import db

Base = declarative_base()


class BaseModel(Base):
    """
    Base class for all models, providing common attributes and methods.

    Attributes:
        id (int): Primary key identifier for the model instance.
        uniq_id (str): Unique identifier for the model instance,
        generated automatically.
        created_at (datetime): Timestamp indicating when the model instance
        was created.
        updated_at (datetime): Timestamp indicating when the model instance was
        last updated.

    Methods:
        save(self):
            Saves the current instance to the database.
        delete(self):
            Deletes the current instance from the database.
        to_dict(self):
            Converts the model instance to a dictionary representation.

    Notes:
        This class should be inherited by all other model classes.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    uniq_id = Column(String(256), unique=True, nullable=False,
                     default=str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow,
                        onupdate=datetime.datetime.utcnow)

    def save(self):
        """Save the current instance to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the current instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """
        Converts the model instance to a dictionary representation.

        Returns:
            dict: Dictionary containing all attributes of the model instance.
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime.datetime):
                result[key] = value.isoformat()
            else:
                result[key] = value
        return result
