"""Test functionality of user endpoint."""

from typing import List
import pytest
from flask import url_for, current_app
from flaskapi.blueprints.v1.user.models import User

from flaskapi.tests.factories.user import UserFactory
from flaskapi.tests.utils import generate_factory_dictionary


@pytest.fixture()
def users():
    return UserFactory.create_batch(size=3)


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestGetUser:
    """Test fetching multiple users."""
    def test_fetching_and_paginating_all_users(self, users, client):
        resp = client.get(url_for('v1.user.users'))

        assert resp.status_code == 200
        assert len(resp.json['data']) == len(users)

        values = {'page': 1, 'total': len(users), 'per_page': 10, 
                  'total_pages': 1}
        for k, v in resp.json['meta_data'].items():
            assert values[k] == v 

    def test_fetching_a_user_detail(self, users, client):
        resp = client.get(url_for('v1.user.single_user', id=users[0].id))
        assert resp.status_code == 200

        data = resp.json
        assert data['id'] == users[0].id


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPostUser:
    def test_creating_new_users(self, client):
        user = generate_factory_dictionary(UserFactory)
        del user['created_at']
        del user['lastlogin_at']
        resp = client.post(url_for('v1.user.users'), json=user)

        assert resp.status_code == 201
        users: List[User] = User.query.all()
        assert len(users) == 1
        assert users[0].first_name == user['first_name']
        assert users[0].last_name == user['last_name']
        assert users[0].username == user['username']
        assert users[0].email == user['email']
        assert users[0].password == user['password']
        assert users[0].phone_number == user['phone_number']
        assert users[0].address == user['address']
