"""Define app test."""
from flask import current_app


def test_app_default_url_works(client):
    """Test that flask app works well."""
    res = client.get('/')
    config = current_app.config

    assert config['TESTING']
    assert config['ENV'] == 'development'
    assert res.status_code == 200
