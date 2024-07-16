"""Implement view for users."""

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, EmailStr
from flaskapi.v1.base_repository import Repository

from flaskapi.v1.user.models import User
from flaskapi.v1.view_manager import DetailView, ListView


class UserRepository(Repository):
    pass
 

class SecuritySchema(BaseModel):
    password: str


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    lastlogin_at: Union[datetime, None] = None

class UserPostSchema(BaseModel):
    """Serialize User object to json format."""
    model_config = ConfigDict(extra='forbid')

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: EmailStr
    password: str
    phone_number: Optional[str] = None
    address: Optional[str] = None


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(extra='forbid')

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class PatchUserSchema(BaseModel):
    """Serialize User object to json format for update."""
    model_config = ConfigDict(extra = 'forbid')

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
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
    update_schema = UpdateUserSchema
