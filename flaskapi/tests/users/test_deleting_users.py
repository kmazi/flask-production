from typing import List
from flask import url_for
import pytest

from flaskapi.blueprints.v1.user.models import User
from flaskapi.tests.factories.user import UserFactory


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestDeleteUser:
    def test_deleting_user_partially(self, client):
        """Successfully delete a user in storage."""
        user = UserFactory.create()
        assert user.deleted_at is None
        resp = client.delete(url_for('v1.user.user', id=user.id), 
                          query_string={'partial': True})
        assert resp.status_code == 204
        users: List[User] = User.query.all()
        assert len(users) == 1
        assert users[0].deleted_at is not None    

    def test_deleting_user_partially_without_passing_partial_querystr(
            self, client):
        """Successfully delete(partial) a user in storage."""
        user = UserFactory.create()
        assert user.deleted_at is None
        resp = client.delete(url_for('v1.user.user', id=user.id))
        assert resp.status_code == 204
        users: List[User] = User.query.all()
        assert len(users) == 1
        assert users[0].deleted_at is not None

    def test_deleting_user_permanently(self, client):
        """Successfully delete permanently a user in storage."""
        user = UserFactory.create()
        assert user.deleted_at is None
        resp = client.delete(url_for('v1.user.user', id=user.id),
                          query_string={'partial': False})
        assert resp.status_code == 204
        users: List[User] = User.query.all()
        assert len(users) == 0  