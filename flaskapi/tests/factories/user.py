"""Define database table factorires."""

from datetime import UTC, datetime, timedelta

import factory

from flaskapi.blueprints.v1.user.models import Security, User
from flaskapi.blueprints.v1.user.util import (CPU_FACTOR, ITERATIONS, REPEAT,
                                              generate_salt, hash_password)
from flaskapi.tests import BaseMeta, ModelFactory


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


SALT = generate_salt()

class SecurityFactory(ModelFactory):
    user_email = factory.Faker('email')
    salt = SALT.decode()
    password = hash_password('password', salt=SALT)[0]
    n = ITERATIONS
    r = CPU_FACTOR
    p = REPEAT
    # Relationships
    user = factory.SubFactory(UserFactory)

    class Meta(BaseMeta):
        model = Security
