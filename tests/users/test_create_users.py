"""Test functionality of user endpoint."""

from typing import List

import pytest
from flask import url_for, current_app

from flaskapi.blueprints.v1.user.models import Security, User
from flaskapi.blueprints.v1.user.util import CPU_FACTOR, ITERATIONS, REPEAT, verify_password


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPostUser:
    def test_creating_new_users_with_valid_json(self, client, 
                                                slim_user):
        """Successfully create a user."""
        slim_user['password'] = 'password'
        resp = client.post(url_for('v1.user.users'), json=slim_user)
        user_res = resp.json
        users: List[User] = User.query.all()
        user = users[0]

        assert resp.status_code == 201
        assert len(users) == 1
        assert user.username == slim_user['username']
        assert user.email == slim_user['email']
        assert user.security.password != slim_user['password']

        assert user_res['username'] == slim_user['username']
        assert user_res['email'] == slim_user['email']
        assert user_res.get('password') is None
        security: Security = user.security
        assert verify_password(slim_user['password'], 
                               pass_hash=security.password, salt=security.salt)

        assert user.security.r == CPU_FACTOR
        assert user.security.n == ITERATIONS
        assert user.security.p == REPEAT
