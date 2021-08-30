"""Define global conftest module."""
import pytest
from flask.logging import logging
from sqlalchemy import inspect

from flaskapp import create_app
from flaskapp.config import TestConfig
from flaskapp.extensions import db

app = create_app(TestConfig)


@pytest.fixture(autouse=True)
def client():
    """Define test client."""
    with app.test_client() as client:
        # run tests in app context
        with app.app_context():
            meta = db.metadata
            insp: Inspector = inspect(db.engine)
            tables = insp.get_table_names()
            if len(tables) > 0:
                # drop tables according to their dependencies in reverse order
                for table in reversed(meta.sorted_tables):
                    if insp.has_table(table):
                        logging.info(".........drop table %s............", table)
                        table.drop(db.engine)
            db.create_all()
            db.session.commit()
            yield client
