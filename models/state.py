#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.city import City
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class for a MySQL database"""
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    def __init__(self, *args, **kwargs):
        """Initialises state"""
        super().__init__(*args, **kwargs)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """returns list of City instances with state_id
            equal to State.id"""
            city_instance_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_instance_list.append(city)
            return city_instance_list
