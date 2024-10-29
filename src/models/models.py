from sqlalchemy import MetaData, Column, String, Integer, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    login = Column(String, unique=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    photo = Column(String, default=None)
    date_registration = Column(DateTime, server_default=func.now())
    refresh_token = Column(String, nullable=False, unique=True)
    deleted = Column(Boolean, default=False)

    user_address = relationship(
        'UserAddress', backref='user', uselist=False, lazy='select')
    user_likes = relationship('Match', backref='likes', foreign_keys='Match.id_to',
                              uselist=True, lazy='select')
    user_liked = relationship('Match', backref='liked', foreign_keys='Match.id_from',
                              uselist=True, lazy='select')


class UserAddress(Base):
    __tablename__ = 'user_address'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    full_address = Column(String, nullable=False, default=None)
    latitude = Column(Integer, nullable=False, default=None)
    longitude = Column(Integer, nullable=False, default=None)


class Match(Base):
    __tablename__ = 'users_matches'

    id_from = Column(Integer, ForeignKey('users.id'), primary_key=True)
    id_to = Column(Integer, ForeignKey('users.id'))
    distance_between = Column(Integer)
