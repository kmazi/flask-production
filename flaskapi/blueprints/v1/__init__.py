"""Define v1 blueprint."""

from flask import Blueprint

from flaskapi.blueprints.v1.user.routes import user_blueprint


v1 = Blueprint('v1', import_name=__name__, url_prefix='/v1')

# Add views to blueprint.
v1.register_blueprint(user_blueprint)
