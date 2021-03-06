"""
This file contains the entry point to our flask application
file import order are:
standard libraries imports
Flask libraries imports
Other Flask non related third-party libraries
Relative and Absolute imports
"""


from flask import jsonify, redirect

from loguru import logger

from config import get_env
from project import create_app, db
from project.models import User, Template


app = create_app(get_env("FLASK_CONFIG"))


@app.shell_context_processor
def make_shell_processor():
    """
    Enables automatic import of the following
    callables when flask shell is executed
    """

    return dict(app=app, db=db, User=User, Template=Template)


@app.route("/", methods=["GET"])
def health_check():
    """
    Checks if API is running
    """
    return jsonify({"status": "success", "msg": "It works"}), 200



@app.errorhandler(404)
def handle_unregistered_url(e):
    """
    Handles application wide 404 errors
    """

    logger.error(e)
    return (
        jsonify(
            {"status": "failed", "msg": "The requested url was not found on the server"}
        ),
        404,
    )


@app.errorhandler(405)
def handle_incorrect_method(e):
    """
    Handles application wide 405 errors
    """

    logger.error(e)
    return (
        jsonify(
            {
                "status": "failed",
                "msg": "The http method used is not allowed for this route",
            }
        ),
        405,
    )


if __name__ == "__main__":
    app.run()
