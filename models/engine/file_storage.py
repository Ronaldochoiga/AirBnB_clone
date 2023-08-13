#!/usr/bin/env python3
"""FileStorage Class.

This module serializes objects to json file
and deserializes json file to objects.
"""
import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Shows procedure of saving and retrieving files

    Attributes:
        __file_path: string - path to the json file
        __objects: dictionary - stores objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """prints all created objs"""
        return FileStorage.__objects

    def new(self, obj):
        """Saves new objects with key class name.id in objects dict"""
        cl_name = type(obj).__name__
        obj_id = obj.id
        key = f"{cl_name}.{obj_id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """Serializes objects to json file"""
        new_dict = {}
        for key, obj in FileStorage.__objects.items():
            new_dict[key] = obj.to_dict()

        with open(FileStorage.__file_path, "w") as f:
            json.dump(new_dict, f)

    def reload(self):
        """Deserializes the json file to objects"""
        try:
            with open(FileStorage.__file_path, "r") as f:
                objects_loaded = json.load(f)

                new_dict = {}
                for key, dict_obj in objects_loaded.items():
                    cl_name = key.split(".")[0]
                    obj = eval(cl_name)(**dict_obj)
                    new_dict[key] = obj
                FileStorage.__objects = new_dict
        except FileNotFoundError:
            pass

    def delete(self, obj):
        """Deletes objects from the json file"""
        cl_name = type(obj).__name__
        obj_id = obj.id
        key = f"{cl_name}.{obj_id}"

        if key in FileStorage.__objects:
            del FileStorage.__objects[key]
            self.save()
            return True

        return False
