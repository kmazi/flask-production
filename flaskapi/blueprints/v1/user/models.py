"""Define auth models."""

from flaskapi.blueprints.v1.base_model import Base
from flaskapi.core.extensions import db


class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(100))
    address = db.Column(db.String(200))
    lastlogin_at = db.Column(db.DateTime)
    salt = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'{self.username}'
