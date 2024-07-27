"""Test functionality of user endpoint."""

import pytest
from flask import url_for


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestGetUser:
    """Test fetching multiple users."""
    def test_pass_fetching_and_paginating_all_users(self, users, client):
        """Successfully fetch and paginate user data."""
        resp = client.get(url_for('v1.user.users'))

        assert resp.status_code == 200
        assert len(resp.json['data']) == len(users)

        values = {'page': 1, 'total': len(users), 'per_page': 10, 
                  'total_pages': 1}
        for k, v in resp.json['meta_data'].items():
            assert values[k] == v 

    def test_Pass_fetching_a_user_detail(self, users, client):
        """Successfully fetch a user detail."""
        sample_user = users[0]
        resp = client.get(url_for('v1.user.user', id=sample_user.id))
        assert resp.status_code == 200

        data = resp.json['data']
        
        assert data['id'] == sample_user.id
        assert sample_user.first_name == data['first_name']
        assert sample_user.last_name == data['last_name']
        assert sample_user.username == data['username']
        assert sample_user.email == data['email']
        assert data.get('password') is None
        assert sample_user.phone_number == data['phone_number']
        assert sample_user.address == data['address']
