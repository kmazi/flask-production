"""Define base database repository."""

from sqlalchemy.orm import Query

from flaskapi.core.extensions import db


class Repository:
    """Define common db queries."""
    def create():
        pass

    def get(Model: db.Model, detail: bool=False, filter=None) -> Query:
        query = db.session.query(Model)
        if filter:
            query = query.filter(*filter)
        return query

    def update(partial: bool=True):
        pass

    def delete(permanent: bool=False):
        pass
