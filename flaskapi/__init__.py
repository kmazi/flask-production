"""Define application factory method."""

import os

from flask import Flask, jsonify

from flaskapi.core.config import Config, DevConfig, TestConfig
from flaskapi.core.exceptions import (handle_500_errors,
                                      validation_error_handler)
from flaskapi.core.extensions import db, migrate
from flaskapi.v1 import V1


def __get_config(env: str) -> Config | DevConfig | TestConfig:
    """Get application config based on app environment.
    -----
    Arguments:
     env - Environment you're working on (dev, test, prod)
    """
    match env.lower():
        case 'dev':
            return DevConfig
        case 'test':
            return TestConfig
        case _:
            return Config


def create_app(env: str = 'prod'):
    """Create flask app.
    -----
    Arguments:
     env - Specify what environment to work on(dev, test, pro). 
        Defaults to prod
    """
    # its important to configure logger
    # before app is created or app.logger accessed.
    from flaskapi.core import logger

    app = Flask(__name__, instance_relative_config=True)

    # Create the instance path if not available
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config.from_object(__get_config(env=env))

    # Add extensions
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)

    # Error handlers
    validation_error_handler(app)
    app.register_error_handler(500, handle_500_errors)

    # Routes

    @app.route('/')
    def welcome():
        return 'Welcome to flask production-ready scaffold.'

    # Register blueprint
    app.register_blueprint(blueprint=V1)

    return app
