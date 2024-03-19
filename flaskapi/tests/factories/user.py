"""Define database table factorires."""

from datetime import UTC, datetime, timedelta

import factory

from flaskapi.blueprints.v1.user.models import Security, User
from flaskapi.tests import BaseFactory


class UserFactory(BaseFactory):
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    lastlogin_at = datetime.now(UTC) - timedelta(days=1)

    class Meta(BaseFactory.Meta):
        model = User


class SecurityFactory(BaseFactory):
    password = factory.Faker('password')

    class Meta(BaseFactory.Meta):
        model = Security
