"""App factory function definition."""

import os

from flask import Flask


def create_app(test_config=None):
    """Create flask app."""
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # Home route
    @app.route("/")
    def welcome():
        return "Welcome to the framework for flask production-ready app"

    return app
