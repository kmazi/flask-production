"""Define common attributes for models."""
from sqlalchemy import text
from flaskapi.core.extensions import db


class Base:
    """Define common attributes of all model classes."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=text('NOW()'),
                                   nullable=False)
    updated_at = db.Column(db.DateTime, server_default=text('NOW()'),
                                   onupdate=text('NOW()'))
    deleted_at = db.Column(db.DateTime, server_default=text('NOW()'),
                                   onupdate=text('NOW()'))
