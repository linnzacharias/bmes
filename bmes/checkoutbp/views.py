from flask import (Blueprint, request,session, render_template, url_for, redirect) 
from datetime import datetime
from bmes.checkoutbp.forms import CheckoutForm
from bmes.checkoutbp import checkout_service

checkout = Blueprint('checkout', __name__, template_folder='templates/checkoutbp')

@checkout.route('/checkout', methods=['GET','POST'])
def checkout_view():
    if request.method == "POST":
        result  = checkout_service.process_checkout(request,session)
        if result:
           return redirect(url_for('checkout.receipt_view'))
        else:
           return redirect(url_for('checkout.receipt_view'))
    else:
       form = CheckoutForm()

       return render_template(
           'checkout.html',
           title='Checkout Page',
           year=datetime.now().year,
           form = form,
         )

@checkout.route('/checkout/receipt')
def receipt_view():

    return render_template(
           'receipt.html',
           title='Receipt Page',
           year=datetime.now().year,
         )
