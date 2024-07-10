"""Define base database repository."""
from sqlalchemy.orm import Query

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
