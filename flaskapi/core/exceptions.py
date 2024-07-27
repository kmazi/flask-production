"""Define error handlers."""

from flask import Flask, jsonify
from pydantic_core import ValidationError


def handle_500_errors(e):
    """Return custom message for 500 errors."""
    return jsonify({'msg': 'An error occurred in the server. Our team is currently working on it.'}), 500


def validation_error_handler(app: Flask):
    """Register client input validation error handler."""
    @app.errorhandler(ValidationError)
    def error_handler(e: ValidationError):
        """Validation error handler."""
        errors = e.errors()

        for error in errors:
            del error['input']
            if error.get('url'):
                del error['url']

        return errors, 422

    return error_handler
