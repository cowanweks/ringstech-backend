from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    render_template,
    Response,
)
from app.models import Image, db
from uuid import uuid4
from app.models import Cart
from app.controllers.login import login, logout


index_route = Blueprint("index_route", __name__, url_prefix="/ringstech/api/v1")


@index_route.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@index_route.route("/signin", methods=["POST", "GET"])
def signin_user():
    """The route that handles user signin"""

    valid, response = login(request.form)

    if valid:
        return jsonify(msg=response), 200

    return jsonify(msg=response), 401


@index_route.route("/signout", methods=["GET"])
def signout_user():
    """The route that handles user signout"""

    valid, response = logout(request.args.get("user_id"))

    if valid:
        return jsonify(msg=response), 200

    return jsonify(msg=response), 500


@index_route.route("/images", methods=["GET"])
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


@index_route.route("/images/<id>", methods=["DELETE"])
def delete_image(id):
    image = Image.query.get(id)

    if not image:
        return jsonify({"error": "Image not found"}), 404

    try:
        db.session.delete(image)
        db.session.commit()
        return jsonify({"message": "Image deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@index_route.route("/images/delete", methods=["DELETE"])
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


@index_route.route("/create_cart")
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


@index_route.route("/check_cart")
def check_cart_exists():
    """Route to create route"""

    cart_id = request.args.get("cart_id")

    if not cart_id:
        return jsonify("Cart ID is required"), 400

    try:

        cart = db.session.query(Cart).filter_by(cart_id=cart_id).scalar()

        if not cart:
            return jsonify("Cart does not exist"), 404

        return jsonify("Cart exists"), 200

    except Exception as ex:
        return jsonify(error=str(ex))
