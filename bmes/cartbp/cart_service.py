import uuid
from bmes.cataloguebp.models import Product
from bmes.cartbp.models import CartStatus, Cart, CartItem
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
    cart = Cart.query.filter_by(unique_cart_id=unique_id).first() #Return None if cart does not exist
    return cart


# Adds Item to cart
def add_to_cart(request, session):

    product_id = request.form['product_id']
    
    product = Product.query.filter_by(id=product_id).first()
    

    #Get the cart
    cart = get_cart(session)
 
    
    if cart:

        cart_item = CartItem.query.filter_by(product_id=product_id).first()

        if cart_item:          
            cart_item.increase_quantity(1)
            db.session.commit()
        else:
            new_cart_item = CartItem()
            new_cart_item.quantity = 1
            new_cart_item.product = product
            new_cart_item.cart = cart
            
            db.session.add(new_cart_item)
            db.session.commit()
    else:
        new_cart = Cart()
        new_cart.unique_cart_id = _unique_cart_id(session)
        new_cart.cart_status = CartStatus.Open 

        db.session.add(new_cart)
        db.session.commit()

        new_cart_item = CartItem()
        new_cart_item.quantity = 1
        new_cart_item.product = product
        new_cart_item.product_id = product.id
        new_cart_item.cart_id= new_cart.id
        new_cart_item.cart = new_cart
        
        db.session.add(new_cart_item)
        db.session.commit()


# Removes Item from cart
def remove_from_cart(request):
    product_id = request.form['product_id']
    cart_item = CartItem.query.filter_by(product_id=product_id)

    cart_item.delete()
    db.session.commit()


# Return Items From User Cart
def get_cart_items(request,session):      

    #Get the cart
    cart = get_cart(session)

    if cart:
        return CartItem.query.filter_by(cart_id=cart.id).all()

# Gets the number of unique items in the User's CArt
def cart_items_count(request,session):
    items = get_cart_items(request,session)
    int = 0
    if items:     
       for item in items:
           int +=item.quantity
    return int


# Get the Cart Total
def get_cart_total(request,session):      

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


