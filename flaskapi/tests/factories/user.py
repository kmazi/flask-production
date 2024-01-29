"""Define database table factorires."""

from datetime import datetime, timedelta, UTC

from factory import Faker

from flaskapi.tests import BaseFactory


class UserFactory(BaseFactory):
    first_name = Faker('name')
    last_name = Faker('name')
    username = Faker('user_name')
    email = Faker('email')
    password = Faker('password')
    phone_number = Faker('phone_number')
    address = Faker('address')
    created_at = datetime.now(UTC) - timedelta(days=3)
    lastlogin_at = datetime.now(UTC) - timedelta(days=2)
