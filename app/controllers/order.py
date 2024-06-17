import json
from typing import NewType
from uuid import uuid4
from app.models import db, Order
from app.forms.order import OrderForm
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


def new_order(data: dict):
    """A controller that handles new user registrations"""


    try:
        new_order_form = OrderForm(data)

        if new_order_form.validate():
            order = Order(
                order_id=str(uuid4()),
                product_id=new_order_form.product_id.data,
                quantity=new_order_form.quantity.data,
                color=new_order_form.color.data,
                shipping_address=new_order_form.shipping_address.data,
            )

            db.session.add(order)
            db.session.commit()
            return True, "Successfully Created new Order!"

        else:
            print(new_order_form.errors)
            return False, new_order_form.errors

    except IntegrityError as ex:
        print(ex)
        return False, "Order already exists!"


def get_order(order_id: str):
    """A controller that handles getting users"""

    try:
        if order_id:
            orders = (
                db.session.execute(
                    db.select(Order)
                    .where(Order.order_id == order_id)
                    .order_by(Order.order_id)
                )
                .scalars()
                .all()
            )
        else:
            orders = (
                db.session.execute(db.select(Order).order_by(Order.order_id))
                .scalars()
                .all()
            )

        serialized_orders = [order.serialize() for order in orders]
        return True, serialized_orders

    except Exception as ex:
        print(ex)
        return False, "Database error occurred!"


def delete_order(order_id: str):
    """A controller that Deletes user"""
    try:
        db.session.execute(db.delete(Order).where(Order.order_id == order_id))
        db.session.commit()
        db.session.close()
        return True, "Successfully Deleted Order!"

    except SQLAlchemyError as ex:
        print(ex)
        db.session.close()
        return False, "Database error occurred!"
