from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db_item = SQLAlchemy()

class Item(db_item.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(240), unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False)