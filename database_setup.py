import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy  import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy .orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()
#C:\Users\ammie\Documents\Udacity course\databases\virtual-machine\Virtual-Machine\vagrant\catalog
class User(Base):
    __tablename__='user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(250), nullable = False)
    last_name = Column(String(250), nullable = False)
    email = Column(String(250))

class Category(Base):
    __tablename__ = 'category'

    #user = relationship(User)
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    #created_by = Column(Integer, ForeignKey('user.id'))
    created_by = Column(Integer, nullable=False)


class Item(Base):
    __tablename__ = 'category_item'
    category = relationship(Category)
    #user = relationship(User)

    id = Column(Integer, primary_key=True)
    item_name = Column(String(250), nullable=False)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    #created_by = Column(Integer, ForeignKey('user.id'))

engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)