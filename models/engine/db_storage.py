#!/usr/bin/python3
"""This module defines the DBStorage engine"""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Class for DBStorage engine"""

    __engine = None
    __session = None

    def __init__(self):
        """Initialisation of DBStorage engine"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on current database session"""
        new_dict = {}
        if cls is None:
            objs = self.__session.query(State).all()
            objs.extend(self.__session.query(City).all())
            objs.extend(self.__session.query(User).all())
            objs.extend(self.__session.query(Place).all())
            objs.extend(self.__session.query(Review).all())
            objs.extend(self.__session.query(Amenity).all())
        else:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls)
            for o in objs:
                key = o.__class__.__name__ + '.' + o.id
                new_dict[key] = o
        return (new_dict)

    def new(self, obj):
        """adds obj to current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit new changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in database and creates new session"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session()

    def close(self):
        """to close current database session"""
        self.__session.close()
