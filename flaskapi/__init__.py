"""Define application factory method."""

import os
from typing import Union

from flask import Flask

from flaskapi.core.config import Config, DevConfig, TestConfig


def get_config(env: str) -> Union[Config, DevConfig, TestConfig]:
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
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.config.from_object(get_config(env=env))
    # Routes

    @app.route('/')
    def welcome():
        return 'Welcome to flask production-ready scaffold'

    return app
