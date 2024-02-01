"""Define helper functionalities here."""

from abc import ABC, abstractclassmethod
from typing import Dict, TypedDict

from flask import jsonify
from pydantic import BaseModel
from sqlalchemy.orm.dynamic import AppenderQuery
from flask_sqlalchemy.pagination import Pagination

from flask.views import MethodView

from flaskapi.blueprints.v1.base_repository import Repository


class PageMetadata(TypedDict):
    page: int
    per_page: int


class ViewMixin:
    """Define helper functions for views."""
    @staticmethod
    def paginate(query: AppenderQuery, serializer: BaseModel, 
                 meta_data: PageMetadata|None=None) -> Dict:
        """Paginate data in using flask sqlalchemy paginate fnx.

        Arguments:
        ---------
        query - The query to paginate
        serializer - Object serializer for paginated results
        page - The page to return
        per_page - Total items in a page

        Returns:
        -------
        Dictionary containing results and metadata (pagination information)
        """
        if meta_data is not None:
            pages: Pagination = query.paginate(error_out=False, **meta_data)
            results = []
            for item in pages.items:
                serialized_item = serializer.model_validate(item)
                results.append(serialized_item.model_dump())

            return {
                "data": results,
                "meta_data": {
                    "page": pages.page,
                    "total": pages.total,
                    "total_pages": pages.pages,
                    "per_page": pages.per_page,
                },
            }
        results = []
        for item in query.all():
            serialized_item = serializer.model_validate(item)
            results.append(serialized_item.model_dump())
        return {"data": results, "count": len(results)}


class ListView(ABC, MethodView, ViewMixin):
    """Validate input and query storage for output."""
    pagination: PageMetadata = {'page': 1, 'per_page': 10}
    
    @property
    @abstractclassmethod
    def model(cls) -> AppenderQuery:
        pass

    @property
    @abstractclassmethod
    def serializer(cls) -> BaseModel:
        pass
    
    @classmethod
    def get(cls):
        """Fetch objects from storage."""
        query = Repository.get(cls.model)
        response = cls.paginate(query=query, serializer=cls.serializer, 
                                meta_data=cls.pagination)
        return jsonify(response)
    
    @classmethod
    def post(cls):
        """Create new object and add to storage."""
        return ''


class DetailView(MethodView):
    """Get, Update or Delete an object in storage."""
    @classmethod
    def get(cls, id: int):
        """Get specif object from storage."""
        obj = Repository.get_one(cls.model, oid=id)
        serialized_item = cls.serializer.model_validate(obj)
        return serialized_item.model_dump()
    
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
