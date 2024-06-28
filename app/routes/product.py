from flask import Blueprint, request, jsonify
from app.controllers.product import (
    new_product,
    delete_product,
    update_product,
)
from app.models import db, Product

# Products blueprint
product_route = Blueprint(
    "product_route", __name__, url_prefix="/api/products"
)


@product_route.post("/")
def new_product_route():
    """New Product"""

    print(request.form)
    valid, msg = new_product(request)

    if valid:
        return jsonify(msg), 201

    return jsonify(msg), 500


@product_route.get("/")
def get_products_route():
    """Get Products"""

    product_id = request.args.get("product_id")
    product_category = request.args.get("category")

    try:
        query = db.select(Product).order_by(Product.product_id)

        if product_id:

            product = db.session.query(Product).filter_by(product_id=product_id).scalar()
            if not product:
                return jsonify(f"Product of id {product_id} can not be found!"), 404

            return jsonify(product.serialize()), 200

        if product_category:

            products = db.session.query(Product).filter_by(product_category=product_category).all()

            if not products:
                return jsonify("Products of category {} can not be found!"),

            serialized_products = [product.serialize() for product in products]
            return serialized_products, 200

        products = db.session.query(Product).all()
        serialized_products = [product.serialize() for product in products]
        return serialized_products, 200

    except Exception as ex:
        print(ex)
        return jsonify(str(ex)), 500


@product_route.put("/")
@product_route.patch("/")
def update_product_route():
    """Update Product"""

    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify("Product ID not provided"), 400

    valid, response = update_product(product_id, request.form)

    if valid:
        return jsonify(msg=response), 201

    else:
        return jsonify(msg=response), 500


@product_route.delete("/")
def delete_product_route():
    """Delete Product"""

    product_id = request.args.get("product_id")

    if not product_id:
        return jsonify("Product ID not provided"), 400

    valid, response = delete_product(product_id)

    if valid:
        return jsonify(msg=response), 200

    else:
        return jsonify(msg=response), 500


@product_route.delete("/delete_all")
def delete_all_products():
    try:
        # Delete all records in the Image table
        num_rows_deleted = db.session.query(Product).delete()
        db.session.commit()
        return jsonify({'message': 'All products deleted successfully', 'num_rows_deleted': num_rows_deleted}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
