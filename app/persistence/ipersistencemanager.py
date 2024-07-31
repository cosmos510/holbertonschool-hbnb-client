from abc import ABC, abstractmethod


class IPersistenceManager(ABC):
    """
    Defines an abstract class IPersistenceManager
    that inherits from the module ABC
    """
    @abstractmethod
    def save(self, entity):
        """Defines the abstract method save, which will be used to save data"""
        pass

    @abstractmethod
    def get(self, entity_id, entity_type):
        """Defines the abstract method get, wich will be used to get data"""
        pass

    @abstractmethod
    def update(self, entity):
        """Defines the abst method update, which will be used to update data"""
        pass

    @abstractmethod
    def delete(self, entity_id, entity_type):
        """Defines the abst method delete, which will be used to delete data"""
        pass
