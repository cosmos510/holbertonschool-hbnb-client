from models.base_model import BaseModel
from sqlalchemy import String, Column, Boolean, DateTime, func
from db import db
import uuid
from werkzeug.security import generate_password_hash


class User(BaseModel, db.Model):
    """
    User class representing user information.

    Attributes:
        id (str): Unique identifier for the user, automatically generated
        using UUID.
        email (str): Email address of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        password (str): Password of the user.
        is_admin (bool): Flag indicating if the user has administrative
        privileges.
        created_at (datetime): Timestamp indicating when the user was created.
        updated_at (datetime): Timestamp indicating when the user was last
        updated.

    Table Name:
        users

    Methods:
        __init__(self, email, first_name, last_name, password):
            Initializes a new instance of the User class.
    """

    __tablename__ = "users"

    id = Column(String(256), nullable=False, default=lambda:
                str(uuid.uuid4()), primary_key=True)
    email = Column(String(256), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(DateTime, onupdate=func.current_timestamp())
    uniq_id = Column(String(256), nullable=False,
                     unique=True, default=lambda: str(uuid.uuid4()))

    def __init__(self, email, first_name, last_name, password, is_admin):
        """
        Initializes a new instance of the User class.

        Args:
            email (str): Email address of the user.
            first_name (str): First name of the user.
            last_name (str): Last name of the user.
            password (str): Password of the user.
        """
        super().__init__()
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.password = generate_password_hash(password)
