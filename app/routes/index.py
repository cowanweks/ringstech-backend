from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    Response, send_from_directory,
)
from app.models import Image, db
from uuid import uuid4
from app.models import Cart
from app.controllers.login import login, logout


index_route = Blueprint("index_route", __name__, url_prefix="/api")


@index_route.get("/images")
def get_image():
    image_id = request.args.get("id")

    if image_id:
        image = Image.query.filter_by(id=image_id).first()

        if not image:
            return "There is no image with that id", 404

        return Response(image.image, mimetype=image.mimetype)

    else:
        image = Image.query.all()
        return jsonify(image)


@index_route.delete("/images/<image_id>")
def delete_image(image_id: str):
    image = Image.query.get(image_id)

    if not image:
        return jsonify({"error": "Image not found"}), 404

    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({"message": "Image deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@index_route.delete("/images/delete")
def delete_all_images():
    try:
        # Delete all records in the Image table
        num_rows_deleted = db.session.query(Image).delete()
        db.session.commit()
        return jsonify(
            {
                "message": "All images deleted successfully",
                "num_rows_deleted": num_rows_deleted,
            }
        ), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@index_route.get("/create_cart")
def create_cart():
    """Route to create route"""

    try:
        cart = Cart(cart_id=str(uuid4()))
        # Save cart to database
        db.session.add(cart)
        db.session.commit()
        return jsonify(session_id=session.sid, cart_id=cart.cart_id)

    except Exception as ex:
        return jsonify(error=str(ex))


@index_route.get("/check_cart/<cart_id>")
def check_cart_exists(cart_id: str):
    """Route to create route"""

    try:

        cart = db.session.query(Cart).filter_by(cart_id=cart_id).scalar()

        if not cart:
            return jsonify(exists=False), 404

        return jsonify(exists=True), 200

    except Exception as ex:
        return jsonify(error=str(ex))
