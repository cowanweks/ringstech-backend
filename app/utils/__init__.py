import os
import pathlib
from uuid import uuid4
from flask import request, current_app
class bcolors:
    """ """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_image(files: dict, file: str):

    if "product_image" in files:

        image = files[f"{file}"]

        if image.filename != "":
            file_name = str(uuid4()) + pathlib.Path(str(image.filename)).suffix

            if allowed_file(
                    filename=file_name,
                    allowed_extensions={
                        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp",
                        "ico", "svg", "psd", "eps", "ai", "raw"
                    },
            ):
                try:
                    image.save(
                        os.path.join(current_app.config["UPLOADS_DIR"], file_name)
                    )

                    return file_name

                except Exception as ex:
                    print(ex)
                    return False

            return False
