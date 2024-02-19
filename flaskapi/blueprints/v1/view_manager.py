"""Define helper functionalities here."""

from abc import ABC, abstractclassmethod
from typing import Dict, TypedDict

from flask import current_app, jsonify, request
from flask.views import MethodView
from flask_sqlalchemy.model import DefaultMeta
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from pydantic import BaseModel
from werkzeug.exceptions import BadRequest

from flaskapi.blueprints.v1.base_repository import Repository


class PageMetadata(TypedDict):
    page: int
    per_page: int


class BaseView(MethodView):
    @classmethod
    def get_model_name(cls):
        name = cls.model.__name__.lower()
        return name
    

class ViewMixin:
    """Define helper functions for views."""
    @staticmethod
    def paginate(query: Query, serializer: BaseModel,
                 meta_data: PageMetadata | None = None, key: str='') -> Dict:
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
        key = 'data' if key == '' else key
        if meta_data is not None:
            pages: Pagination = query.paginate(error_out=False, **meta_data)
            results = []
            for item in pages.items:
                serialized_item = serializer.model_validate(item)
                results.append(serialized_item.model_dump())

            return {
                key: results,
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
        return {key: results, "count": len(results)}


class ListView(ABC, BaseView, ViewMixin):
    """Validate input and query storage for output."""
    pagination: PageMetadata = {'page': 1, 'per_page': 10}

    @property
    @abstractclassmethod
    def model(cls) -> DefaultMeta:
        pass

    @property
    @abstractclassmethod
    def serializer(cls) -> BaseModel:
        pass

    @classmethod
    def get(cls):
        """Fetch objects from storage."""
        query = Repository.get_all(cls.model)
        response = cls.paginate(query=query, serializer=cls.serializer,
                                meta_data=cls.pagination, 
                                key=cls.get_model_name() + 's')
        return jsonify(response)

    @classmethod
    def post(cls):
        """Create new object and add to storage."""
        # Validate incoming request and deserilize into pydantic model
        data: BaseModel = cls.serializer(**request.json)
        # serialize into dictionary and load data into database
        model = data.model_dump()
        obj = cls.model(**model).save()

        model['id'] = obj.id
        response = {cls.get_model_name(): model}
        return jsonify(response), 201


class DetailView(BaseView):
    """Get, Update or Delete an object in storage."""
    @classmethod
    def get(cls, id: int):
        """Get specif object from storage."""
        obj = Repository.get_one(cls.model, oid=id)
        serialized_item = cls.serializer.model_validate(obj)
        response = {cls.get_model_name(): serialized_item.model_dump()}
        return jsonify(response)

    @classmethod
    def put(cls, id: int):
        """Update all values to new data."""
        obj = Repository.get_one(cls.model, oid=id)
        # Validate, deserialize input data into pydantic model
        # and then dump it as dict.
        data: Dict = cls.serializer(**request.json).model_dump()
        # Get all public attributes of model updated.
        Repository.update(obj=obj, data=data, partial=False)
        return '', 204

    @classmethod
    def patch(cls, id: int):
        """Update object in storage partially."""
        obj = Repository.get_one(cls.model, oid=id)
        ObjSchema = getattr(cls, 'patch_serializer', 'serializer')
        # Validate, deserialize input data into pydantic model
        # and then dump it as dict.
        data: Dict = ObjSchema(**request.json).model_dump()
        obj = Repository.update(obj=obj, data=data, partial=True)
        # Deserialize model object.
        serialized_obj = ObjSchema.model_validate(obj).model_dump()
        response = {cls.get_model_name(): serialized_obj}
        return jsonify(response)

    @classmethod
    def delete(cls, id: int, partial: bool=True):
        """Delete object from storage."""
        obj = Repository.get_one(cls.model, oid=id)
        Repository.delete(obj=obj, partial=partial)
        return '', 204
