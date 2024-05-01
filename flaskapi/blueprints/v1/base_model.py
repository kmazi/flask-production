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
        for key, val in kwargs.items():
            setattr(self, key, val)

        db.session.add(self)
        db.session.commit()
        return self
    
    @staticmethod
    def update(obj, data: Dict):
        """Update object completely or partially."""
        for attribute, val in data.items():
                setattr(obj, attribute, val)            

        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj, permanent: bool=False):
        """Delete obj permanently or setting delete attr to true."""
        if permanent:
            db.session.delete(obj)
        else:
            obj.deleted_at = datetime.now(UTC)
            db.session.add(obj)
        db.session.commit()
