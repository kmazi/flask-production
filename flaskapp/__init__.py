"""App factory function definition."""

import os

from flask import Flask

from flaskapp import extensions
from flaskapp.config import Config


def create_app(config=Config):
    """Create flask app.
    Parameters:
    ---
    config - object:- Defines config for flask app
    """
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config.from_object(config)
    # initialize extensions
    db = extensions.db
    db.init_app(app)
    extensions.migrate.init_app(app, db)
    # Routes
    @app.route('/')
    def welcome():
        return 'Welcome to the framework for flask production-ready app'
    with app.app_context():
        from . import resources

    return app
