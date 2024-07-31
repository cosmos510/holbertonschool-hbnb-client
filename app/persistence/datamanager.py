import json
import datetime
from persistence.ipersistencemanager import IPersistenceManager
import os
from db import db


class DataManager(IPersistenceManager):
    """
    Defines the subclass DataManager that inherits from
    IPersistenceManager
    """

    def __init__(self, flag):
        """
        Initializes DataManager instance.

        Args:
        flag (str): Flag parameter used to set file path.

        Sets up DataManager instance with appropriate file path and
        determines persistence mode based on environment variable
        or defaults to 'file'.

        Attributes:
        persistence_mode (str): Mode of persistence for data storage,
            either 'file' or 'database'.
    """
        self.set_file_path(flag)


    def set_file_path(self, flag):
        """Sets in which json file data will be managed based on a flag"""
        if flag == 1:
            self.file_path = "/home/hbnb/hbnb_data/User.json"
        elif flag == 2:
            self.file_path = "/home/hbnb/hbnb_data/Place.json"
        elif flag == 3:
            self.file_path = "/home/hbnb/hbnb_data/Amenity.json"
        elif flag == 4:
            self.file_path = "/home/hbnb/hbnb_data/Review.json"
        elif flag == 5:
            self.file_path = "/home/hbnb/hbnb_data/cities.json"

        else:
            raise ValueError(f"Unsupported flag value: {flag}")

    def save(self, entity):
        """
        Saves the entity to the appropriate storage (file or database).

        Args:
            entity (dict or SQLAlchemy model):
            The entity to save. If it's a dictionary, it will be saved to
            a file.
            If it has a '__tablename__' attribute (indicating it's an
            SQLAlchemy model),
            it will be saved to the database.

        Raises:
            ValueError: If the entity type is not supported.
        """
        if isinstance(entity, dict):
            self.save_to_file(entity)
        elif hasattr(entity, '__tablename__'):
            self.save_to_database(entity)
        else:
            raise ValueError("Unsupported entity type")

    def get(self, entity, id):
        """
        Retrieves the entity from the appropriate storage (file or database)
        based on its id.

        Args:
            entity (type): The type of entity to retrieve. If it's a
            dictionary, it will be retrieved from a file.
            If it has a '__tablename__' attribute
                    (indicating it's an SQLAlchemy model), it will be
                    retrieved from the database.
            id (str): The unique identifier of the entity.

        Returns:
            dict or SQLAlchemy model: The retrieved entity data.

        Raises:
            ValueError: If the entity type is not supported.
        """
        if isinstance(entity, dict):
            return self.get_from_file(entity, id)
        elif hasattr(entity, '__tablename__'):
            return self.get_from_database(entity, id)
        else:
            raise ValueError("Unsupported entity type")
        
        
    def delete(self, entity, id):
        """
        Deletes the entity from the appropriate storage (file or database)
        based on its id.

        Args:
            entity (type): The type of entity to delete. If it's a dictionary,
            it will be deleted from a file.
            If it has a '__tablename__' attribute (indicating
                        it's an SQLAlchemy model), it will be deleted from
                        the database.
            id (str): The unique identifier of the entity to delete.

        Raises:
            ValueError: If the entity type is not supported.
        """
        if isinstance(entity, dict):
            self.delete_from_file(entity, id)
        elif hasattr(entity, '__tablename__'):
            self.delete_from_database(entity, id)
        else:
            raise ValueError("Unsupported entity type")

    def update(self, entity, id, data):
        """
        Updates the entity in the appropriate storage (file or database) based
        on its id.

        Args:
            entity (type): The type of entity to update. If it's a dictionary,
            it will be updated in a file.
            If it has a '__tablename__' attribute (indicating it's an
            SQLAlchemy model), it will be updated in the database.
            id (str): The unique identifier of the entity to update.
            data (dict): The data to update the entity with.

        Raises:
            ValueError: If the entity type is not supported.
        """
        if isinstance(entity, dict):
            self.update_file(entity, id)
        elif hasattr(entity, '__tablename__'):
            self.update_database(entity, id, data)
        else:
            raise ValueError("Unsupported entity type")

    def save_to_file(self, entity):
        """
        Saves the entity to a JSON file.

        Args:
            entity (dict): Entity data to be saved into the file.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does
            not exist.
            Exception: For any other unexpected error during file operation.
        """
        try:
            if os.path.isfile(self.file_path):
                with open(self.file_path, 'r', encoding='UTF-8') as f:
                    data = json.load(f)
            else:
                data = []

            data.append(entity)

            with open(self.file_path, 'w', encoding='UTF-8') as f:
                json.dump(data, f, indent=4)

        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e

    def get_from_file(self, entity, id):
        """
        Retrieves the entity from a JSON file based on its id.

        Args:
            entity (type): Type of entity to retrieve (not directly used in
            file
            mode).
            id (str): Unique identifier of the entity.

        Returns:
            dict: Retrieved entity data.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
        """
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                for item in data:
                    if item["uniq_id"] == id:
                        return item
        except FileNotFoundError:
            pass

    def delete_from_file(self, entity, id):
        """
        Deletes the entity from a JSON file based on its id.

        Args:
            entity (type): Type of entity to delete (not directly used in file
            mode).
            id (str): Unique identifier of the entity.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
        """

        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
                for item in data:
                    if item["uniq_id"] == id:
                        data.remove(item)
                        with open(self.file_path, 'w', encoding='UTF-8') as f:
                            json.dump(data, f, indent=4)
                        return
        except FileNotFoundError:
            pass

    def update_file(self, entity, id):
        """
        Updates the entity in a JSON file based on its id.

        Args:
            entity (dict): Updated entity data to replace existing data.
            id (str): Unique identifier of the entity.

        Raises:
            FileNotFoundError: If the file specified by self.file_path does not
            exist.
        """
        try:
            with open(self.file_path, 'r', encoding='UTF-8') as f:
                data = json.load(f)
            for item in data:
                if item["uniq_id"] == id:
                    data.remove(item)
                    entity["updated_at"] = datetime.datetime.now().isoformat()
                    data.append(entity)
                    with open(self.file_path, 'w', encoding='UTF-8') as f:
                        json.dump(data, f, indent=4)
                    return
        except FileNotFoundError:
            pass

    def save_to_database(self, entity):
        """
        Saves the entity to the database.

        Args:
            entity (SQLAlchemy model): Entity object to be saved.
        """
        db.session.add(entity)
        db.session.commit()

    def get_from_database(self, entity, id):
        """
        Retrieves the entity from the database based on its id.

        Args:
            entity (type): Type of entity to retrieve (used in database mode).
            id (str): Unique identifier of the entity.

        Returns:
            SQLAlchemy model: Retrieved entity object.
        """
        return db.session.query(entity).filter_by(id=id).first()

    def delete_from_database(self, entity, id):
        """
        Deletes the entity from the database based on its id.

        Args:
            entity (type): Type of entity to delete (used in database mode).
            id (str): Unique identifier of the entity.
        """

        entity_to_delete = db.session.query(entity).filter_by(id=id).first()
        if entity_to_delete:
            db.session.delete(entity_to_delete)
            db.session.commit()

    def update_database(self, entity, id, data):
        """
        Updates the entity in the database based on its id.

        Args:
            entity (SQLAlchemy model): Updated entity object to replace
            existing data.
            id (str): Unique identifier of the entity.
        """
        entity_to_update = db.session.query(entity).filter_by(id=id).first()
        if entity_to_update:
            for key, value in data.items():
                setattr(entity_to_update, key, value)
            db.session.commit()
