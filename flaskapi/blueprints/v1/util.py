"""Define helper functionalities here."""

from flask.views import MethodView


class ListView(MethodView):
    """Validate input and query storage for output."""
    @classmethod
    def get(cls):
        """Fetch objects from storage."""
        return ''
    
    @classmethod
    def post(cls):
        """Create new object and add to storage."""
        return ''


class DetailView(MethodView):
    """Get, Update or Delete an object in storage."""
    @classmethod
    def put(cls, id: int):
        """Update values to new data."""
        return ''
    
    @classmethod
    def patch(cls, id: int):
        """Update object in storage partially."""
        return ''
    
    @classmethod
    def delete(cls, id: int):
        """Delete object from storage."""
        return ''
