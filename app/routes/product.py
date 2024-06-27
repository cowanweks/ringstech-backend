from flask import Blueprint, request, jsonify
from app.controllers.product import (
    new_product,
    delete_product,
    update_product,
)
from app.models import db, Product

# Units blueprint
product_route = Blueprint(
    "product_route", __name__, url_prefix="/ringstech/api/v1/products"
)


@product_route.route("/", methods=["POST"])
def new_product_route():
    """New Product"""

    print(request.form)
    valid, msg = new_product(request)

    if valid:
        return jsonify(msg), 201

    return jsonify(msg), 500


@product_route.route("/", methods=["GET"])
def get_products_route():
    """Get Units"""

    product_id = request.args.get("product_id")
    product_category = request.args.get("category")

    try:
        query = db.select(Product).order_by(Product.product_id)

        if product_id:
            query = query.where(Product.product_id == product_id)
        if product_category:
            query = query.where(Product.product_category == product_category)

        products = db.session.execute(query).scalars().all()
        serialized_products = [product.serialize() for product in products]

        return serialized_products, 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


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


@product_route.route("/delete", methods=["DELETE"])
def delete_all_products():
    try:
        # Delete all records in the Image table
        num_rows_deleted = db.session.query(Product).delete()
        db.session.commit()
        return jsonify({'message': 'All products deleted successfully', 'num_rows_deleted': num_rows_deleted}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
