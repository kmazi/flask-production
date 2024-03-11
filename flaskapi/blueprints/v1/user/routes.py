"""Define user blueprint."""
from flask import Blueprint

from flaskapi.blueprints.v1.user.views import ListUsers, SingleUser

user_blueprint = Blueprint('user', import_name=__name__, url_prefix='/users')

# Add views to blueprint.
user_blueprint.add_url_rule('/', view_func=ListUsers.as_view('users'))
user_blueprint.add_url_rule('/<int:id>', view_func=SingleUser.as_view(
    'user'))