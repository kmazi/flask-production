"""Define configurations for different environments."""
import os

class Config:
    """Base app configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False