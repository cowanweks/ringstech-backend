import os
from uuid import uuid4
from flask import (
    Blueprint,
    current_app,
    request,
    jsonify,
    render_template,
    send_from_directory,
)
import pathlib
from app.controllers.login import login, logout
from app.utils import allowed_file


index_route = Blueprint("index_route", __name__, url_prefix="/ringstech/api/v1")


@index_route.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@index_route.route("/uploads", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if "image" in request.files:

            image = request.files["image"]

            if image.filename != "":
                file_name = str(uuid4()) + pathlib.Path(str(image.filename)).suffix

                if allowed_file(
                    filename=file_name,
                    ALLOWED_EXTENSIONS={"txt", "pdf", "png", "jpg", "jpeg", "gif"},
                ):
                    try:
                        image.save(
                            os.path.join(current_app.config["UPLOADS_DIR"], file_name)
                        )
                        return jsonify(file_name=file_name), 201

                    except Exception as ex:
                        print(ex)
                        return jsonify(f"{str(ex)}"), 500

                return "File type not supported!", 500

            return "Please upload an image", 500

        return "Please upload an image", 500

    image = request.args.get("image")
    return send_from_directory(current_app.config["UPLOADS_DIR"], f"{image}")


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
