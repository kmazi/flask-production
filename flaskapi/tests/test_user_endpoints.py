"""Test functionality of user endpoint."""

import pytest
from flask import url_for

from flaskapi.tests.factories.user import UserFactory


@pytest.fixture()
def users():
    return UserFactory.create_batch(size=3)


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestGetUserList:
    """Test fetching multiple users."""
    def test_fetching_all_users(self, users, client):
        resp = client.get(url_for('v1.user.users'))

        assert resp.status_code == 200
        assert len(resp.json['data']) == len(users)
