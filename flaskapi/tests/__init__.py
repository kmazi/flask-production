"""Define base factory."""

import factory
from flaskapi.core.extensions import db

from flaskapi.blueprints.v1.user.models import User

class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'