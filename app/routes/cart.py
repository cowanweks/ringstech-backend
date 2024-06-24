from flask import (
    Blueprint,
    request,
    jsonify,
    session
)
import requests
from uuid import uuid4
from app.models import Order
from app.forms.order import OrderForm
from sqlalchemy.exc import IntegrityError
from app.models import db, Cart, CartItem, Product

BASE_URL = "https://samsungrepair-backend-35d7356462b8.herokuapp.com//"

cart_route = Blueprint("cart_route", __name__, url_prefix="/ringstech/api/v1/cart")


@cart_route.route("/", methods=["POST"])
def add_item_to_cart_route():
    """Route to add new item to cart"""
    cart_id = request.args.get("cart_id")
    product_id = request.args.get("product_id")
    quantity = request.args.get("quantity")
    color = request.args.get("color")

    if not cart_id:
        return jsonify(error="Cart Id not provided")

    if not product_id:
        return jsonify(error="Product Id not provided")

    if not quantity:
        return jsonify(error="Item Quantity not provided")

    product = (db.session.query(Product).filter_by(product_id=product_id).scalar())

    cart_item = CartItem(item_id=str(uuid4()),
                         product_id=product_id,
                         product_name=product.product_name,
                         color=color,
                         quantity=quantity,
                         price=product.product_unit_price,
                         cart_id=cart_id
                         )

    try:

        if db.session.query(CartItem).filter_by(product_id=product_id, color=color).count() > 0:
            (db.session.query(CartItem).filter_by(product_id=product_id, color=color)
             .update({'quantity': CartItem.quantity + quantity}))
        else:
            db.session.add(cart_item)

        db.session.commit()

        return jsonify(msg="Successfully Added item {} to cart {}".format(cart_item.item_id, cart_item.cart_id)), 200

    except Exception as ex:
        print(ex)
        return jsonify(error=str(ex))


@cart_route.route("/", methods=["GET"])
def view_cart_route():
    """Route to View Cart"""
    cart_id = request.args.get("cart_id")

    if not cart_id:
        return jsonify(error="Please provide Cart ID")

    query = db.select(CartItem).order_by(CartItem.item_id)
    query = query.where(CartItem.cart_id == cart_id)

    cart = db.session.execute(query).scalars().all()
    serialized_cart_items = [item.serialize() for item in cart]

    if not serialized_cart_items:
        return []

    return jsonify(serialized_cart_items)


@cart_route.route("/checkout", methods=["POST"])
def checkout_cart():
    """New Order"""

    cart_id = request.args.get("cart_id")

    if not cart_id:
        return jsonify(error="Cart ID Required")

    cart = db.session.query(Cart).filter_by(cart_id=cart_id).scalar()

    if not cart:
        return jsonify(error="Cart does not exist!")

    total_amount = int(cart.total_amount)

    try:
        new_order_form = OrderForm(request.form)

        payment_url = (BASE_URL + "/ringstech/api/v1/payment/pay?phone_number={}&total_amount={}"
         .format(new_order_form.mpesa_number.data, total_amount))

        print(payment_url)

        if new_order_form.validate():
            order = Order(
                order_id=str(uuid4()),
                cart_id=cart_id,
                first_name=new_order_form.first_name.data,
                middle_name=new_order_form.middle_name.data,
                last_name=new_order_form.last_name.data,
                street_address=new_order_form.street_address.data,
                city=new_order_form.city.data,
                state_or_province=new_order_form.state_or_province.data,
                email_address=new_order_form.email_address.data,
                phone_number=new_order_form.phone_number.data,
                total_amount=cart.total_amount,
                zip_code=new_order_form.zip_code.data
            )

            db.session.add(order)
            db.session.commit()

            # Make Payment
            response = (requests.get(payment_url))

            if response.status_code == 200:
                db.session.query(Order).filter_by(cart_id=cart_id).update({'payment_status': 'PAID'})
                return jsonify("Successfully Created new Order!"), 200

            return jsonify(response.content.decode())

        else:
            print(new_order_form.errors)
            return jsonify(error=new_order_form.errors), 500

    except IntegrityError as ex:
        print(ex)
        return jsonify(error="Order already exists!"), 500
