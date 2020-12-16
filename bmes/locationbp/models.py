from sqlalchemy.types import Enum
from datetime import datetime
from bmes.sharedbp import db
import enum

# Status
class AddressType(enum.Enum):
    Delivery=1
    Billing=2
    Unknown=3

# Base Model
class Base(db.Model):
     __abstract__ = True
     id = db.Column(db.Integer, primary_key=True)
     created_date = db.Column(db.DateTime(), default=datetime.now())
     modified_date = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
     is_deleted = db.Column(db.Boolean())

# Address Model
class Address(Base):
    __tablename__ = 'addresses' 
    name = db.Column(db.String(50),nullable=True)
    address_line_1  = db.Column(db.String(150))  
    address_line_2 = db.Column(db.String(150),nullable=True)
    city  = db.Column(db.String(50))  
    state  = db.Column(db.String(50)) 
    country = db.Column(db.String(50))
    zip_code = db.Column(db.String(50))
    address_type  = db.Column('address_type', Enum(AddressType))
