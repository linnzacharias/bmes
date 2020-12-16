from bmes.sharedbp import db
from sqlalchemy.types import Enum
from datetime import datetime
import enum

# Status
class StatusType(enum.Enum):
    Active=1
    InActive=2

product_category = db.Table('product_category',
 db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)   
)

product_brand = db.Table('product_brand',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('brand_id', db.Integer, db.ForeignKey('brands.id'), primary_key=True)
)

# Base Model
class Base(db.Model):
     __abstract__ = True
     id = db.Column(db.Integer, primary_key=True)
     created_date = db.Column(db.DateTime(), default=datetime.now())
     modified_date = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
     is_deleted = db.Column(db.Boolean())


     # Category Model
class Category(Base):
    __tablename__ = 'categories' 

    name  = db.Column(db.String(50), unique=True, nullable=False)
    slug =  db.Column(db.String(50), unique=True, nullable=False)
    description  = db.Column(db.Text())
    meta_description  = db.Column(db.String(500))
    meta_keywords  = db.Column(db.String(500))
    category_status  = db.Column('category_status', Enum(StatusType))

    def __repr__(self):
        return self.name

# Brand Model
class Brand(Base):
    __tablename__ = 'brands'

    name  = db.Column(db.String(50), unique=True, nullable=False)
    slug =  db.Column(db.String(50), unique=True, nullable=False)
    description  = db.Column(db.Text())
    meta_description  = db.Column(db.String(500))
    meta_keywords  = db.Column(db.String(500))
    brand_status  = db.Column('brand_status', Enum(StatusType))

    def __repr__(self):
        return self.name

# Product Model
class Product(Base):
    __tablename__ = 'products'

    name  = db.Column(db.String(50), unique=True, nullable=False)
    slug =  db.Column(db.String(50), unique=True, nullable=False)
    description  = db.Column(db.Text())
    meta_description  = db.Column(db.String(500))
    meta_keywords  = db.Column(db.String(500))
    sku = db.Column(db.String(100))
    model = db.Column(db.String(200))
    price = db.Column(db.Float())
    old_price = db.Column(db.Float())
    image_url = db.Column(db.String(250))
    is_bestseller = db.Column(db.Boolean())     
    is_featured = db.Column(db.Boolean())    
    quantity = db.Column(db.Integer())
    categories = db.relationship('Category',secondary=product_category,lazy='subquery')
    brands = db.relationship('Brand',secondary=product_brand,lazy='subquery')
    product_status  = db.Column('product_status', Enum(StatusType))
    
    def sale_price(self):           
        if self.old_price > self.price:                
            return self.price           
        else:                
            return None

    def __repr__(self):
        return self.name