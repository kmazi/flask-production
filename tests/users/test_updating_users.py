from typing import List

import pytest
from flask import url_for

from flaskapi.blueprints.v1.user.models import User
from tests.factories.user import UserFactory


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPatchUser:
    def test_updating_user_partially(self, client):
        """Successfully update a user in storage."""
        update = {'first_name': 'Kingsley', 'last_name': 'Mazi'}
        user = UserFactory.create()
        user_id = user.id
        resp = client.patch(url_for('v1.user.user', id=user_id),
                            json=update)

        updated_user = User.query.filter_by(id=user_id).first()

        assert resp.status_code == 200
        assert updated_user.first_name == update['first_name']
        assert updated_user.last_name == update['last_name']


@pytest.mark.usefixtures('app_ctx', 'setup')
class TestPutUser:
    def test_updating_user(self, client, user_dictionary):
        """Successfully update a user in storage."""
        del user_dictionary['created_at']
        del user_dictionary['updated_at']
        del user_dictionary['lastlogin_at']
        del user_dictionary['email']
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
