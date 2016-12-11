from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databasesetup import *

engine = create_engine('sqlite:///itemcatalog.db')
DBSession = sessionmaker(bind = engine)
session = DBSession()

session.query(Category).delete()
session.query(Item).delete()

session.add_all([
    Category(name = "Kanto"),
    Category(name = "Johto"),
    Category(name = "Hoenn"),
    Category(name = "Sinnoh"),
    Category(name = "Unova"),
    Category(name = "Kalos"),
    Category(name = "Alola")])
session.commit()