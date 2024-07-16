"""Test functionality of user endpoint."""

from typing import List

import pytest
from flask import url_for

from flaskapi.v1.user.models import Security, User
from flaskapi.v1.user.util import (CPU_FACTOR, ITERATIONS, REPEAT,
                                   verify_password)


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPostUser:
    def test__pass_creating_new_users_with_valid_json(self, client,
                                                slim_user):
        """Successfully create a user."""
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

    @pytest.mark.parametrize('field', ['password', 'email'])
    def test_fail_creating_user_without_fields(self, client, slim_user,
                                                 field):
        """."""
        del slim_user[field]
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 422
        assert resp.json == [{'loc': [field], 'msg': 'Field required', 
                              'type': 'missing'}]
    @pytest.mark.run
    def test_fail_creating_user_with_invalid_email(self, client, slim_user):
        """."""
        slim_user['email'] = 'mazimia.ugo@com'
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 422
    
    @pytest.mark.parametrize('field', ['first_name', 'last_name', 'username',
                                       'phone_number', 'address'])
    def test_pass_creating_user_without_fields(self, client, slim_user,
                                               field):
        """."""
        del slim_user[field]
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json[field] is None
        assert field not in slim_user.keys()
