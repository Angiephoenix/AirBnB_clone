#!/usr/bin/python3

"""base model of the airbnb project"""

from datetime import datetime
import uuid
import models

time_fmt = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel:
    """parent class of the airbnb project"""

    def __init__(self, *args, **kwargs):
        """Constructor for BaseModel objects"""

        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if hasattr(self, "created_at")\
                    and isinstance(self.created_at, str):
                self.created_at = datetime.strptime(
                    kwargs['created_at'], time_fmt)

            if hasattr(self, "updated_at")\
                    and isinstance(self.updated_at, str):
                self.updated_at = datetime.strptime(
                    kwargs['updated_at'], time_fmt)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """string representation of of the BaseModel object"""
        return f"{[type(self).__class__.__name__]} {(self.id)} {self.__dict__}"

    def save(self):
        """updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """returns a dict containing namespace attributes of the object"""
        my_dict = {k: v for k, v in self.__dict__.items()}
        my_dict['__class__'] = str(type(self).__name__)
        my_dict["created_at"] = self.created_at.isoformat()
        my_dict["updated_at"] = self.updated_at.isoformat()

        return my_dict
