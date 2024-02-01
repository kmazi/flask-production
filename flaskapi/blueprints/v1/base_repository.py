"""Define base database repository."""

from sqlalchemy.orm import Query

from flaskapi.core.extensions import db


class Repository:
    """Define common db queries."""
    def create():
        pass

    def get(Model: db.Model) -> Query:
        query = db.session.query(Model)
        return query
    
    def get_one(Model: db.Model, oid):
        data = db.session.get(Model, oid)
        return data

    def update(partial: bool=True):
        pass

    def delete(permanent: bool=False):
        pass
