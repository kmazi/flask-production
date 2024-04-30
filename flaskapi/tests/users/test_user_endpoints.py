"""Test functionality of user endpoint."""

from typing import List

import pytest
from flask import url_for

from flaskapi.blueprints.v1.user.models import User
from flaskapi.tests.factories.user import UserFactory


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestGetUser:
    """Test fetching multiple users."""
    def test_fetching_and_paginating_all_users(self, users, client):
        """Successfully fetch and paginate user data."""
        resp = client.get(url_for('v1.user.users'))

        assert resp.status_code == 200
        assert len(resp.json['users']) == len(users)

        values = {'page': 1, 'total': len(users), 'per_page': 10, 
                  'total_pages': 1}
        for k, v in resp.json['meta_data'].items():
            assert values[k] == v 

    def test_fetching_a_user_detail(self, users, client):
        """Successfully fetch a user detail."""
        resp = client.get(url_for('v1.user.user', id=users[0].id))
        assert resp.status_code == 200

        data = resp.json['user']
        
        assert data['id'] == users[0].id
        assert users[0].first_name == data['first_name']
        assert users[0].last_name == data['last_name']
        assert users[0].username == data['username']
        assert users[0].email == data['email']
        assert users[0].password == data['password']
        assert users[0].phone_number == data['phone_number']
        assert users[0].address == data['address']


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPatchUser:
    def test_updating_user_partially(self, client):
        """Successfully update a user in storage."""
        update = {'first_name': 'Kingsley', 'last_name': 'Mazi'}
        user = UserFactory.create()
        resp = client.patch(url_for('v1.user.user', id=user.id), 
                          json=update)
        updated_user = User.query.filter_by(id=user.id).first()
        assert resp.status_code == 200
        user = resp.json['user']
        assert updated_user.first_name == update['first_name']
        assert updated_user.last_name == update['last_name']


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPutUser:
    def test_updating_user(self, client, user_dictionary):
        """Successfully update a user in storage."""
        user = UserFactory.create()
        resp = client.put(url_for('v1.user.user', id=user.id), 
                          json=user_dictionary)
        assert resp.status_code == 204
        users: List[User] = User.query.all()
        user = users[0]
        assert len(users) == 1
        assert user.address == user_dictionary['address']
        assert user.first_name == user_dictionary['first_name']
        assert user.last_name == user_dictionary['last_name']
        assert user.email == user_dictionary['email']


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
