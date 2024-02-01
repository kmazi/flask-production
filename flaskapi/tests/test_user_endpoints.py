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
