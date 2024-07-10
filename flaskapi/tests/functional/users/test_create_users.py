"""Test functionality of user endpoint."""

from typing import List

import pytest
from flask import url_for

from flaskapi.v1.user.models import Security, User
from flaskapi.v1.user.util import (CPU_FACTOR, ITERATIONS, REPEAT,
                                   verify_password)


@pytest.mark.usefixtures('app_ctx', 'setup')
@pytest.mark.one
class TestPostUser:
    def test__pass_creating_new_users_with_valid_json(self, client,
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

    def test_fail_creating_user_without_password(self, client, slim_user):
        """."""
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 401
        assert resp.json == [{'loc': ['password'], 'msg': 'Field required', 
                              'type': 'missing'}]
        
    def test_fail_creating_user_without_email(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['email']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 401
        assert resp.json == [{'loc': ['email'], 'msg': 'Field required', 
                              'type': 'missing'}]
        
    def test_pass_creating_user_without_firstname(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['first_name']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json['first_name'] is None
        assert 'first_name' not in slim_user.keys()

    def test_pass_creating_user_without_lastname(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['last_name']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json['last_name'] is None
        assert 'last_name' not in slim_user.keys()

    def test_pass_creating_user_without_username(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['username']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json['username'] is None
        assert 'username' not in slim_user.keys()

    def test_pass_creating_user_without_phone_number(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['phone_number']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json['phone_number'] is None
        assert 'phone_number' not in slim_user.keys()

    def test_pass_creating_user_without_address(self, client, slim_user):
        """."""
        slim_user['password'] = 'password'
        del slim_user['address']
        resp = client.post(url_for('v1.user.users'), json=slim_user)

        assert resp.status_code == 201
        assert resp.json['address'] is None
        assert 'address' not in slim_user.keys()
