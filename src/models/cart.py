from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer
from models.user import *

class Cart(db_user.Model):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=False, nullable=False)
    item_id = Column(Integer, unique=False, nullable=False)