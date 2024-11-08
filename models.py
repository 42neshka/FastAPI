from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    age = Column(Integer)


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    executor_id = Column(Integer, ForeignKey('users.id'), index=True)
    theme = Column(String)
    deadline = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'), index=True)

    author = relationship('User', foreign_keys=[author_id])
    executor = relationship('User', foreign_keys=[executor_id])


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True, unique=True)
    role_id = Column(Integer, ForeignKey('roles.id'), index=True, unique=True)


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name_role = Column(String, index=True)
















