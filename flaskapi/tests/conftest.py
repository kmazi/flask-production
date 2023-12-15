"""Setup test environment."""
from typing import Generator

from flask import Flask
from flask.testing import FlaskClient

from flaskapi import create_app
from flaskapi.core.extensions import db

import pytest

@pytest.fixture(scope='package')
def app() -> Flask:
    app = create_app(env='test')
    return app

@pytest.fixture
def app_ctx(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield

@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    """Define test client."""
    with app.test_client() as client:
        yield client

@pytest.fixture
def setup() -> Generator[None, None, None]:
    db.create_all()
    yield
    db.session.remove()
    db.drop_all()
