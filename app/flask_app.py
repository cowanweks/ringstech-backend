import os
import secrets
from flask import Flask
from .extensions import cors, db, sess, folder_setup
from app.routes import (
    index_route,
    cart_route,
    user_route,
    role_route,
    order_route,
    product_route,
    payment_route
)  # Routes
from app.errors.error_handlers import not_found  # Error Handlers
from app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from app.utils.app_utils import app_setup
from app.utils import bcolors
from cachelib.file import FileSystemCache


# Create application and return it.
@app_setup
def create_app() -> Flask:
    app = Flask(__name__)

    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config["SESSION_TYPE"] = "cachelib"
    app.config["SESSION_USE_SIGNER"] = True
    app.config["SESSION_SERIALIZATION_FORMAT"] = "json"
    app.config["SESSION_CACHELIB"] = FileSystemCache(threshold=500, cache_dir="sessions")

    # Prevent redirects in blueprints
    app.url_map.strict_slashes = False
    app.add_url_rule(
        "/ringstech/api/v1", endpoint="api_index", view_func=lambda: "API Home Page"
    )

    # Set the application configuration
    if os.getenv("ENV") == "production":
        app.config.from_object(ProductionConfig)

    elif os.getenv("ENV") == "development":
        app.config.from_object(DevelopmentConfig)

    else:
        app.config.from_object(TestingConfig)

    # Register blueprints
    app.register_blueprint(index_route)
    app.register_blueprint(cart_route)
    app.register_blueprint(user_route)
    app.register_blueprint(role_route)
    app.register_blueprint(order_route)
    app.register_blueprint(product_route)
    app.register_blueprint(payment_route)

    # Register error handlers
    app.register_error_handler(404, not_found)

    db.init_app(app)
    cors.init_app(app)
    sess.init_app(app)
    folder_setup.init_app(app)  # Set the templates and static directories

    with app.app_context():
        db.create_all()

    print(
        bcolors.OKGREEN
        + f"""[*] - You are running {app.config.get('APP_NAME')} in {app.config.get('ENV')} on HOST {app.config.get("HOST")} on PORT {app.config.get("PORT")} !"""
    )

    return app
