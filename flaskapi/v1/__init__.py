"""Define v1 blueprint."""

from flask import Blueprint

from flaskapi.v1.user.routes import user_blueprint

V1 = Blueprint('v1', import_name=__name__, url_prefix='/v1')

# Add views to blueprint.
V1.register_blueprint(user_blueprint)
