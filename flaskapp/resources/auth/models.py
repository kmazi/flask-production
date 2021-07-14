"""Define auth models."""

from flaskapp.extensions import db
from sqlalchemy.sql.expression import text


class Base:
    """Define common attributes of all model classes."""

    id = db.Column(db.Integer, primary_key=True)
    created_on = db.Column(db.DateTime, server_default=text("NOW()"), nullable=False)
    updated_on = db.Column(
        db.DateTime, server_default=text("NOW()"), onupdate=text("NOW()")
    )


class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{username}'
