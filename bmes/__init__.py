"""
The flask application package.
"""

import os
from flask import request,session, Flask
from bmes.sharedbp import db
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from bmes.cataloguebp.models import Brand, Category, Product
from bmes.userbp.models import Customer, Person
from bmes.locationbp.models import Address
from bmes.cataloguebp.views import catalogue
from bmes.cartbp.views import cart
from bmes.locationbp.views import location
from bmes.userbp.views import user
from bmes.orderbp.views import order
from bmes.checkoutbp.views import checkout
from bmes.cartbp import cart_service

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

#App Secret Key
app.config['SECRET_KEY'] = '95371e2f-a487-4e22-a9e2-8b6356b85453'

#Blueprint Registration
app.register_blueprint(catalogue)
app.register_blueprint(cart)
app.register_blueprint(location)
app.register_blueprint(user)
app.register_blueprint(order)
app.register_blueprint(checkout)

#Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'bmeswebapp.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Registering The Product Catalogue Models to the Admin Module
admin = Admin(app)
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Brand, db.session))
admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Person, db.session))
admin.add_view(ModelView(Address, db.session))


db.init_app(app)
migrate = Migrate(app, db)

import bmes.views

@app.context_processor
def inject_context():
    return {
              'cart_item_count': cart_service.cart_items_count(request,session),
              'cart_total': cart_service.get_cart_total(request, session),
              'cart_items': cart_service.get_cart_items(request,session),
           }