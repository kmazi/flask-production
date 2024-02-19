"""Define base database repository."""

from datetime import datetime, UTC
from typing import Dict

from sqlalchemy.orm import Query
from werkzeug.exceptions import BadRequest

from flaskapi.core.extensions import db


class Repository:
    """Define common db queries."""
    @staticmethod
    def get_all(Model) -> Query:
        """Fetch all data in storage."""
        query = db.session.query(Model)
        return query
    
    @staticmethod
    def get_one(Model, oid):
        """Fetch an object with id from storage."""
        data = db.session.get(Model, oid)
        return data

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
                    raise BadRequest(f"'{attribute}' is invalid or missing.")

        obj = obj.save()
        return obj

    @staticmethod
    def delete(obj, partial: bool=False):
        """Delete obj permanently or setting delete attr to true."""
        if (partial):
            obj.deleted_at = datetime.now(UTC)
            obj.save()
        else:
            db.session.delete(obj)
            db.session.commit()
