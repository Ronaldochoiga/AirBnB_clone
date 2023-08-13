#!/usr/bin/env python3
"""BaseModel Class.

this module has definition for other subclasses
"""
import models
import uuid
from datetime import datetime

time_format = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """Shows blueprints of subclasses

    Attributes:
        id: string - assign uuid4 which is random
        created_at: datetime - give with the current datetime when an
                    object is created
        updated_at: datetime - given with the current datetime
                    object is created and it will be updated each time
                    you change objects
    """

    def __init__(self, *args, **kwargs):
        """An object constructor"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    if key == "created_at" or key == "updated_at":
                        self.__dict__[key] = datetime.strptime(
                            value, time_format)
                    else:
                        self.__dict__[key] = value
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """A str rep of objects"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Updates  current datetime and save object"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Prints modified dict with all att of an obj"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = type(self).__name__
        new_dict["created_at"] = self.created_at.strftime(time_format)
        new_dict["updated_at"] = self.updated_at.strftime(time_format)
        return new_dict
