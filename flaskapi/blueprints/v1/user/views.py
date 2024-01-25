"""Implement view for users."""

from flaskapi.blueprints.v1.user.models import User
from flaskapi.blueprints.v1.util import DetailView, ListView



class UserSerializer:
    """Serialize User object to json format."""
    pass


class ListUsers(ListView):
    """Create and fetch users."""
    model = User
    serializer = UserSerializer


class SingleUser(DetailView):
    """Fetch update and delete a user."""
    model = User
    serializer = UserSerializer
