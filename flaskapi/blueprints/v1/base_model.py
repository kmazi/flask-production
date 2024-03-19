"""Define common attributes for models."""
from datetime import UTC, datetime
from typing import Dict

from sqlalchemy import text
from werkzeug.exceptions import BadRequest

from flaskapi.core.extensions import db


class Base:
    """Define common attributes of all model classes."""

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=text('NOW()'),
                                   nullable=False)
    updated_at = db.Column(db.DateTime, server_default=text('NOW()'),
                                   onupdate=text('NOW()'))
    deleted_at = db.Column(db.DateTime)

    def save(self, **kwargs):
        for key, val in kwargs:
            if val is not None:
                setattr(self, key, val)

        db.session.add(self)
        db.session.commit()
        return self
    
    @staticmethod
    def update(obj, data: Dict, partial: bool=True):
        """Update object completely or partially."""
        if (partial):
            for attribute, val in data.items():
                if val is not None:
                    setattr(obj, attribute, val)
        else:
            model = obj.__class__
            model_attributes = list(
            filter(lambda x: x[0] != '_', model.__dict__.keys()))
            for attribute in model_attributes:
                try:
                    setattr(obj, attribute, data[attribute])
                except KeyError:
                    raise BadRequest(f"'{attribute}' is missing.")

        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj, partial: bool=False):
        """Delete obj permanently or setting delete attr to true."""
        if (partial):
            obj.deleted_at = datetime.now(UTC)
            db.session.add(obj)
        else:
            db.session.delete(obj)
        db.session.commit()
