"""Test functionality of user endpoint."""

from typing import List

import pytest
from flask import url_for

from flaskapi.blueprints.v1.user.models import User
from flaskapi.blueprints.v1.user.util import CPU_FACTOR, ITERATIONS, REPEAT


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPostUser:
    def test_creating_new_users_with_valid_json(self, client, 
                                                slim_user):
        """Successfully create a user."""
        slim_user['password'] = 'password'
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        resp_user = resp.json
        assert resp.status_code == 201
        users: List[User] = User.query.all()
        assert len(users) == 1
        assert users[0].username == resp_user['username']
        assert users[0].email == resp_user['email']
        assert users[0].security.password is not None
        assert users[0].security.r == CPU_FACTOR
        assert users[0].security.n == ITERATIONS
        assert users[0].security.p == REPEAT
