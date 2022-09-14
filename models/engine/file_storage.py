#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Set in __objects obj with key <obj_class_name>.id"""
        if obj:
            self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialises __objects to the JSON file path"""
        with open(self.__file_path, 'w') as f:
            json_temp = {}
            json_temp.update(self.__objects)
            for key, val in json_temp.items():
                json_temp[key] = val.to_dict()
            json.dump(json_temp, f)

    def reload(self):
        """Deserialise json file to __objects, if it exists"""
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                json_dict = json.load(f)
                for value in json_dict.values():
                    cls = value['__class__']
                    self.new(eval('{}({})'.format(cls, '**value')))
        except (FileNotFoundError):
            pass

    def delete(self, obj=None):
        """deletes obj from __objects"""
        if obj is not None:
            try:
                key = obj.__class__.__name__ + "." + obj.id
                if key in self.__objects:
                    del self.__objects[key]
            except (KeyError):
                pass
