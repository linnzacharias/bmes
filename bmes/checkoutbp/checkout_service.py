import uuid
from bmes.cataloguebp.models import Product
from bmes.cartbp.models import Cart, CartItem
from bmes.locationbp.models import Address
from bmes.orderbp.models import OrderStatus, OrderItem, Order
from bmes.userbp.models import GenderType, Customer, Person
from bmes.checkoutbp.forms import CheckoutForm
from bmes.sharedbp import db


UNIQUE_CART_ID_SESSION_KEY = 'unique_cart_id'


# get the current user's unique cart id, sets new one if blank 
def _unique_cart_id(session):
     if UNIQUE_CART_ID_SESSION_KEY not in session:            
         session[UNIQUE_CART_ID_SESSION_KEY] = _generate_unique_id()    
     return session[UNIQUE_CART_ID_SESSION_KEY]


def _generate_unique_id():
    u_id = uuid.uuid1()
    u_id_string = str(u_id)
    return u_id_string

# Gets the cart
def get_cart(session): 
    unique_id =_unique_cart_id(session)
    cart = Cart.query.filter_by(unique_cart_id=unique_id).first()
    return cart


# Process checkout
def process_checkout(request,session):
        form = CheckoutForm(request.form)
        if form.validate():
            first_name = form.first_name.data
            middle_name = form.middle_name.data
            last_name = form.last_name.data
            email = form.email.data
            address_line_1 = form.address_line_1.data
            address_line_2 = form.address_line_2.data
            city = form.city.data
            state = form.state.data
            country = form.country.data
            zip_code = form.zip_code.data
       

            person = Person()
            person.first_name = first_name
            person.middle_name = middle_name
            person.last_name = last_name
            person.email_address = email
            person.gender = GenderType.Unknown
            person.is_deleted = False

            db.session.add(person)
            db.session.commit()
          
            address = Address()
            address.address_line_1 = address_line_1
            address.address_line_2 = address_line_2
            address.city = city
            address.state = state
            address.country = country
            address.zip_code = zip_code
            address.is_deleted = False

            db.session.add(address)
            db.session.commit()

            customer = Customer()
            customer.person_id = person.id
            customer.person = person
            customer.is_deleted = False
            customer.addresses.append(address)

            db.session.add(customer)
            db.session.commit()

            cart = get_cart(session)

            if cart:
               cart_total = get_cart_total(session)

               shipping_cost = 0.00

               order_total = cart_total + shipping_cost

               order = Order()
               order.order_total = order_total   
               order.order_item_total = cart_total
               order.order_status = OrderStatus.Submitted               
               order.shipping_charge = shipping_cost
               order.delivery_address_id = address.id
               order.delivery_address = address
               order.customer_id = customer.id
               order.customer = customer

               db.session.add(order)
               db.session.commit()

               cart_items = get_cart_items(session)

               if cart_items:
                  for cart_item in cart_items:

                     order_item = OrderItem()
                     order_item.order_id = order.id
                     order_item.quantity = cart_item.quantity
                     order_item.price = cart_item.price()
                     order_item.product_id = cart_item.product.id

                     db.session.add(order_item)
                     db.session.commit()

               db.session.delete(cart)
               db.session.commit()
               return True       
            else:
               return False


# Return Items From User Cart
def get_cart_items(session):      

    #Get the cart
    cart = get_cart(session)

    if cart:
        return CartItem.query.filter_by(cart_id=cart.id).all()


# Get the Cart Total
def get_cart_total(session):      

    #Get the cart
    cart = get_cart(session)
    cart_total = 0.00

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        for item in cart_items:
            cart_total += item.cart_item_total()
        return cart_total
    else:
        return cart_total



