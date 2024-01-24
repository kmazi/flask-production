"""Define common attributes for models."""
from sqlalchemy import Column, text
from flaskapi.core.extensions import db


class Base:
    """Define common attributes of all model classes."""

    id: Column = db.Column(db.Integer, primary_key=True)
    created_at: Column = db.Column(db.DateTime, server_default=text('NOW()'),
                                   nullable=False)
    updated_at: Column = db.Column(db.DateTime, server_default=text('NOW()'),
                                   onupdate=text('NOW()'))
    deleted_at: Column = db.Column(db.DateTime, server_default=text('NOW()'),
                                   onupdate=text('NOW()'))
