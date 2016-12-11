from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship

decbase = declarative_base()


class User(decbase):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    email = Column(String(255), nullable = False)


class Category(decbase):
    __tablename__ = 'category'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    items = relationship("Item", back_populates = "category")


class Item(decbase):
    __tablename__ = 'item'

    id = Column(Integer, primary_key = True)
    name = Column(String(255), nullable = False)
    description = Column(String(2048))
    created = Column(DateTime(timezone=True), default=func.now())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates = "items")
    user_id = Column(Integer, ForeignKey('user.id'))

engine = create_engine('sqlite:///itemcatalog.db')
decbase.metadata.create_all(engine)
