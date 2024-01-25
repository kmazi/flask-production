"""Define auth models."""

from flaskapi.blueprints.v1.base_model import Base
from flaskapi.core.extensions import db


class User(Base, db.Model):
    """Define user model."""
    __tablename__ = "users"
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    lastlogin_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'{self.username}'
