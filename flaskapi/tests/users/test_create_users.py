"""Test functionality of user endpoint."""

from typing import Dict, List

import pytest
from flask import url_for

from flaskapi.blueprints.v1.user.models import User
from flaskapi.blueprints.v1.user.util import CPU_FACTOR, ITERATIONS, REPEAT


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPostUser:
    def test_creating_new_users_with_valid_json(self, client, 
                                                user_dictionary):
        """Successfully create a user."""
        user: Dict = user_dictionary
        del user['created_at']
        del user['lastlogin_at']
        user['password'] = 'password'
        resp = client.post(url_for('v1.user.users'), json=user)

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
