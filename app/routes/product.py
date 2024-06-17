from flask import Blueprint, request, jsonify
from app.controllers.product import new_product, get_products, delete_product, update_product

# Units blueprint
product_route = Blueprint("product_route", __name__, url_prefix="/ringstech/api/v1/products")


@product_route.route("/", methods=["POST"])
def new_product_route():
    """New Unit"""

    """
    ImmutableMultiDict([('available_colors',
    '["red", "Green", "Yellow"]'), ('product_category',
    'accessory'), ('description', 'This is Arek'), ('is_available', 'False'),
     ('product_name', 'samsung'), ('product_unit_price', '5000'), ('in_stock', '4'),
      ('brand', 'Samsung'), ('display', 'Guerrilla Screen')])
    """

    valid, msg = new_product(request.form, request.files)

    if valid:
        return jsonify(msg=msg), 201

    return jsonify(msg=msg), 500


@product_route.route("/", methods=["GET"])
def get_products_route():
    """Get Units"""

    valid, response = get_products(request.args)

    if valid:
        return jsonify(response), 200

    return jsonify(msg=response), 500


@product_route.route("/", methods=["PUT", "PATCH"])
def update_product_route():
    """Update Unit"""

    valid, response = update_product(request.args.get("product_id"), request.form)

    if valid:
        return jsonify(msg=response), 201

    else:
        return jsonify(msg=response), 500


@product_route.route("/", methods=["DELETE"])
def delete_product_route():
    """Delete Unit"""

    valid, response = delete_product(request.args.get("product_id"))

    if valid:
        return jsonify(msg=response), 200

    else:
        return jsonify(msg=response), 500

