"""Implement fixtures for user endpoint."""

import pytest

from flaskapi.tests.factories.user import UserFactory
from flaskapi.tests.utils import generate_factory_dictionary


@pytest.fixture()
def users():
    return UserFactory.create_batch(size=3)


@pytest.fixture()
def user_dictionary():
    user = generate_factory_dictionary(UserFactory)
    
    user['created_at'] = user['created_at'].isoformat()
    user['lastlogin_at'] = user['lastlogin_at'].isoformat()
    user['updated_at'] = user['updated_at'].isoformat()
    return user
