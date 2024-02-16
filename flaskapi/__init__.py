"""Define application factory method."""

import os
from typing import Union

from flask import Flask, jsonify

from flaskapi.blueprints.v1 import V1
from flaskapi.core.config import Config, DevConfig, TestConfig
from flaskapi.core.extensions import db, migrate


def __get_config(env: str) -> Union[Config, DevConfig, TestConfig]:
    """Get application config based on app environment."""
    match env.lower():
        case 'dev':
            return DevConfig
        case 'test':
            return TestConfig
        case _:
            return Config


def create_app(env: str = 'prod'):
    """Create flask app."""
    # Import log config
    from flaskapi.core import logger  # its important to configure logger

    # before app is created or app.logger accessed.
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
    @app.errorhandler(code_or_exception=400)
    def add_400_error_handler(error):
        return jsonify({'detail': str(error)}), 400

    # Routes
    @app.route('/')
    def welcome():
        return 'Welcome to flask production-ready scaffold.'
    
    # Register blueprint
    app.register_blueprint(blueprint=V1)

    return app
