from flask import request, jsonify, Blueprint
from app.models import db, Order

order_route = Blueprint("order_route", __name__, url_prefix="/ringstech/api/v1/order")


@order_route.route("/", methods=["GET"])
def get_orders_route():
    """Get Orders"""

    order_id = request.args.get("order_id")

    try:
        if order_id:

            orders = db.session.query(Order).filter_by(Order.order_id == order_id).scalar()

        else:

            orders = db.session.query(Order).order_by(Order.order_id).all()

        serialized_orders = [order.serialize() for order in orders]
        return jsonify(serialized_orders), 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.route("/", methods=["DELETE"])
def delete_order_route():
    """Delete Order"""

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify(error="Order ID Required")

    try:
        db.session.execute(db.delete(Order).where(Order.order_id == order_id))
        db.session.commit()
        return jsonify("Successfully Deleted Order!"), 300

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@order_route.route("/complete_order", methods=["GET"])
def complete_order():
    order_id = request.args.get("order_id")

    try:
        if order_id is None:
            return jsonify("Cart ID Not Provided")

        db.session.query(Order).filter(Order.order_id == order_id).update({'completed': True})
        db.session.commit()

    except Exception as ex:
        print(ex)
        return jsonify(str(ex))


@order_route.route("/update_payment_status", methods=["GET"])
def update_payment_status():
    order_id = request.args.get("order_id")

    try:
        if order_id is None:
            return jsonify("Cart ID Not Provided")

        db.session.query(Order).filter(Order.order_id == order_id).update({'completed': True})
        db.session.commit()

    except Exception as ex:
        print(ex)
        return jsonify()
