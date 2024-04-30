"""Implement view for users."""

from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict
from flaskapi.blueprints.v1.base_repository import Repository

from flaskapi.blueprints.v1.user.models import User
from flaskapi.blueprints.v1.view_manager import DetailView, ListView


class UserRepository(Repository):
    pass
 

class SecuritySchema(BaseModel):
    password: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    phone_number: str | None = None
    address: str | None = None
    lastlogin_at: Union[datetime, None] = None

class UserPostSchema(BaseModel):
    """Serialize User object to json format."""
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str
    phone_number: str | None = None
    password: str
    address: str | None = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    lastlogin_at: Union[datetime, None] = None


class PatchUserSchema(BaseModel):
    """Serialize User object to json format for update."""
    model_config = ConfigDict(from_attributes=True)

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    password: str | None = None
    phone_number: str | None = None
    address: str | None = None
    created_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None
    deleted_at: Union[datetime, None] = None
    lastlogin_at: Union[datetime, None] = None


class ListUsers(ListView):
    """Create and fetch users."""
    model = User
    post_schema = UserPostSchema
    response_schema = UserResponseSchema


class SingleUser(DetailView):
    """Fetch update and delete a user."""
    model = User
    response_schema = UserResponseSchema
    patch_schema = PatchUserSchema
