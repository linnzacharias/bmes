from flask import (Blueprint, request, render_template, url_for, redirect) 
from datetime import datetime
from bmes.cartbp import cart_service

cart = Blueprint('cart', __name__, template_folder='templates/cartbp')

@cart.route('/cart', methods=['GET','POST'])
def cart_detail():

    if request.method == "POST":
        cart_service.remove_from_cart(request)

        return render_template(
           'cart_detail.html',
           title='Product Page',
           year=datetime.now().year,
         )
    else:
        return render_template(
           'cart_detail.html',
           title='Product Page',
           year=datetime.now().year,
         )