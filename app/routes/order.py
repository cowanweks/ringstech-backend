from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db
from app.models import Order

# Orders blueprint
order_route = Blueprint("order_route", __name__, url_prefix="/ringstech/api/v1/orders")


@order_route.route("/", methods=["GET"])
def get_orders_route():
    """Get Orders"""

    order_id = request.args.get("order_id")

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
        return jsonify(serialized_orders), 200

    except Exception as ex:
        print(ex)
        return jsonify("Database error occurred! {}".format(ex)), 500


@order_route.route("/", methods=["DELETE"])
def delete_order_route():
    """Delete Unit"""

    order_id = request.args.get("order_id")

    if not order_id:
        return jsonify(error="Order ID Required")

    try:
        db.session.execute(db.delete(Order).where(Order.order_id == order_id))
        db.session.commit()
        return jsonify("Successfully Deleted Order!"), 300

    except SQLAlchemyError as ex:
        print(ex)
        return jsonify("Database error occurred!"), 500
