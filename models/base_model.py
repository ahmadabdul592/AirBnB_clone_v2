#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from uuid import uuid4
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for name, value in kwargs.items():
                if name == 'created_at' or name == 'updated_at':
                    value = datetime.strptime(
                                    value, "%Y-%m-%dT%H:%M:%S.%f")
                if name != "__class__":
                    setattr(self, name, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        my_dict = self.__dict__.copy()
        my_dict.pop("_sa_instance_state", None)
        return '[{}] ({}) {}'.format(type(self).__name__, self.id, my_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        m_dict = {}
        m_dict.update(self.__dict__)
        m_dict.update({'__class__': (str(type(self)).split('.')[-1])
                      .split('\'')[0]})
        m_dict['created_at'] = self.created_at.isoformat()
        m_dict['updated_at'] = self.updated_at.isoformat()
        m_dict.pop("_sa_instance_state", None)
        return m_dict

    def delete(self):
        """Deletes the current instance from storage"""
        models.storage.delete(self)
