"""Define database table factorires."""

from datetime import UTC, datetime, timedelta

import factory

from flaskapi.blueprints.v1.user.models import Security, User
from flaskapi.blueprints.v1.user.util import generate_salt, hash_password
from flaskapi.tests import BaseMeta, ModelFactory


class SecurityFactory(ModelFactory):
    password = hash_password('password', salt=generate_salt())[0]

    class Meta(BaseMeta):
        model = Security


class UserFactory(ModelFactory):
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    address = factory.Faker('address')
    lastlogin_at = datetime.now(UTC) - timedelta(days=1)

    class Meta(BaseMeta):
        model = User
