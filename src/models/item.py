from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=False, nullable=False)
    description = Column(String(240), unique=False, nullable=False)
    price = Column(Integer, unique=False, nullable=False)