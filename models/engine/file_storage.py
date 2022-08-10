#!/usr/bin/python3
"""FilesStorage module"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """serializes and deserializes instances to json files
    Attributes:
        __file_path: string - path to the JSON file
        __objects: dictionary - empty but will store all objects' namespace
    """

    __file_path = "file.json"
    __objects = dict()

    def all(self):
        """returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        object_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(
            object_name, obj.id)] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        object_dict = FileStorage.__objects

        obj_dict = {obj: object_dict[obj].to_dict()
                    for obj in object_dict.keys()}
        with open(FileStorage.__file_path, 'w') as filename:
            json.dump(obj_dict, filename)

    def reload(self):
        """ deserializes the JSON file to __objects if it exists"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as filename:
                json_object = json.load(filename)
            for k, v in json_object.items():
                cls_name = v["__class__"]
                del v["__class__"]
                self.new(eval(cls_name)(**v))
        except FileNotFoundError:
            pass
