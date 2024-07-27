"""Define common attributes for models."""
from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from flaskapi.core.extensions import db


class Base:
    """Define common attributes of all model classes."""

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        server_default=text('NOW()'), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        server_default=text('NOW()'), onupdate=text('NOW()'))
    deleted_at: Mapped[Optional[datetime]] = mapped_column()

    def save(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def update(obj, data: Dict):
        """Update object completely or partially."""
        for attribute, val in data.items():
            setattr(obj, attribute, val)

        db.session.add(obj)
        db.session.commit()
        return obj

    @staticmethod
    def delete(obj, permanent: bool = False):
        """Delete obj permanently or setting delete attr to true."""
        if permanent:
            db.session.delete(obj)
        else:
            obj.deleted_at = datetime.now()
            db.session.add(obj)
        db.session.commit()
