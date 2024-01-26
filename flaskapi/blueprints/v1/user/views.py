"""Implement view for users."""

from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict

from flaskapi.blueprints.v1.user.models import User
from flaskapi.blueprints.v1.util import DetailView, ListView



class UserSerializer(BaseModel):
    """Serialize User object to json format."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str | None
    last_name: str | None
    username: str
    email: str
    phone_number: str | None
    address: str | None
    created_at: datetime
    updated_at: Union[datetime, None]
    deleted_at: Union[datetime, None]


class ListUsers(ListView):
    """Create and fetch users."""
    model = User
    serializer = UserSerializer


class SingleUser(DetailView):
    """Fetch update and delete a user."""
    model = User
    serializer = UserSerializer
