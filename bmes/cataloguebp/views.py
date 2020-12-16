from flask import (Blueprint, request,session, render_template, url_for, redirect) 
from datetime import datetime
from bmes.cataloguebp import catalogue_service
from bmes.cartbp import cart_service

catalogue = Blueprint('catalogue', __name__, template_folder='templates/cataloguebp')

@catalogue.route('/catalogue', methods=['GET','POST'])
@catalogue.route('/catalogue/<category_slug>/<brand_slug>/', methods=['GET','POST'])
def catalogue_view(category_slug='all-categories', brand_slug='all-brands'): 

     if request.method == 'POST':

         cart_service.add_to_cart(request, session) #We are adding item to the cart

         #Fetching products from the catalogue service
         page_object = catalogue_service.fetch_products(request, category_slug, brand_slug)

         return render_template(
           'catalogue.html',
           title='Product Page',
           year=datetime.now().year,
           page_object= page_object,
           selected_category=category_slug,
           selected_brand=brand_slug,
         )
     else:        
         page_object = catalogue_service.fetch_products(request, category_slug, brand_slug)

         return render_template(
           'catalogue.html',
           title='Product Page',
           year=datetime.now().year,
           page_object= page_object,
           selected_category=category_slug,
           selected_brand=brand_slug,
         )


@catalogue.route('/catalogue/products/<product_slug>/') 
def product_detail_view(product_slug):
    return render_template(
           title='Product Page',
           year=datetime.now().year,
         )