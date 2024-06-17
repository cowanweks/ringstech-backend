""" """
from flask import Blueprint, request, jsonify
from app.controllers.order import new_order, get_order, delete_order

# Units blueprint
order_route = Blueprint("order_route", __name__, url_prefix="/ringstech/api/v1/orders")


@order_route.route("/", methods=["POST"])
def new_order_route():
    """New Unit"""

    valid, msg = new_order(request.form)

    if valid:
        return jsonify(msg=msg), 201

    return jsonify(msg=msg), 500


@order_route.route("/", methods=["GET"])
def get_orders_route():
    """Get Units"""

    valid, response = get_order(request.args.get("order_id"))

    if valid:
        return jsonify(data=response), 200

    return jsonify(msg=response), 500


@order_route.route("/", methods=["DELETE"])
def delete_order_route():
    """Delete Unit"""

    valid, response = delete_order(request.args.get("order_id"))

    if valid:
        return jsonify(msg=response), 200

    else:
        return jsonify(msg=response), 500

