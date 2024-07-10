"""Define application factory method."""

import os

from flask import Flask, jsonify

from flaskapi.v1 import V1
from flaskapi.core.config import Config, DevConfig, TestConfig
from flaskapi.core.extensions import db, migrate


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
