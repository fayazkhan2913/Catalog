import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()

# creating class 'user' with tablename 'user' and giving columns to table.


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))

# creating class 'MovieGenre' with tablename 'moviegenre' and inserting columns


class MovieGenre(Base):
    __tablename__ = 'moviegenre'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="moviegenre")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }

# creating class 'MovieName' with tablename 'moviename' and inserting columns


class MovieName(Base):
    __tablename__ = 'moviename'
    id = Column(Integer, primary_key=True)
    poster = Column(String(250))
    name = Column(String(350), nullable=False)
    year = Column(String(150))
    rating = Column(String(150))
    budget = Column(String(10))
    gross = Column(String(250))
    date = Column(DateTime, nullable=False)
    moviegenreid = Column(Integer, ForeignKey('moviegenre.id'))
    moviegenre = relationship(
        MovieGenre, backref=backref('moviename', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="moviename")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'poster': self.poster,
            'name': self. name,
            'year': self. year,
            'rating': self. rating,
            'budget': self. budget,
            'gross': self. gross,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///movies.db')
Base.metadata.create_all(engin)
