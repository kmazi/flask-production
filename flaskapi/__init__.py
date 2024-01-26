"""Define application factory method."""

import os
from typing import Union

from flask import Flask
from flaskapi.blueprints.v1 import v1

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

    # Routes
    @app.route('/')
    def welcome():
        return 'Welcome to flask production-ready scaffold.'
    
    # Register blueprint
    app.register_blueprint(blueprint=v1)

    return app
