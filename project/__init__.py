"""
This package contains the initialization
of neccessary libraries required for the
successful startup of the application
"""


from flask import Flask

from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from config import load_configs


db = MongoEngine()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(config_name):
    """
    A factory pattern implementation
    of the Flask app
    """

    app = Flask(__name__)
    app.config.from_object(
        load_configs[config_name]
    )  # configures app instance for different enviroments
    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from .Auth import auth as auth_blueprint
    from .Template import template as template_blueprint

    app.register_blueprint(template_blueprint, url_prefix="/api/v1/template")
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")

    return app
