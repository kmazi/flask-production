"""Define auth models."""

from sqlalchemy import Column
from flaskapi.blueprints.base_model import Base
from flaskapi.core.extensions import db


class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name: Column = db.Column(db.String(50))
    last_name: Column = db.Column(db.String(50))
    username: Column = db.Column(db.String(50), nullable=False)
    email: Column = db.Column(db.String(100), nullable=False)
    password: Column = db.Column(db.String(), nullable=False)
    phone_number: Column = db.Column(db.String(100), nullable=True)
    address: Column = db.Column(db.String(200, nullable=True))
    lastlogin_at: Column = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'{self.username}'
