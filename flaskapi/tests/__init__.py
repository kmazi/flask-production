"""Define base factory."""

from datetime import UTC, datetime, timedelta

import factory

from flaskapi.core.extensions import db


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    created_at = factory.Faker('date_time_between',
                               start_date=datetime.now(UTC)-timedelta(
                                   days=100))
    updated_at = factory.LazyAttribute(
        lambda obj: obj.created_at + timedelta(days=2))
    
    class Meta:
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = 'flush'
