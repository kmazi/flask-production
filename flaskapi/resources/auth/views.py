from flask import current_app as app
from . import models


@app.route('/users')
def users():
    """Define user signin."""
    users = models.User.query.all()
    return {"data": users}
