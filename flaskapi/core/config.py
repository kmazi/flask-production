"""Define configurations for different environments."""
import os

class Config:
    """Setup Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class DevConfig(Config):
    """Setup Development configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestConfig(Config):
    """Setup Testing configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')
    SERVER_NAME = os.getenv('SERVER_NAME')
    TESTING = True
