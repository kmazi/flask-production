"""Define helper functionalities here."""

from abc import ABC, abstractmethod
from typing import Dict, Optional, Type, TypedDict

from flask import jsonify, request
from flask.views import MethodView
from flask_sqlalchemy.model import DefaultMeta
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from pydantic import BaseModel, ValidationError

from flaskapi.v1.base_model import Base
from flaskapi.v1.base_repository import Repository


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
                 meta_data: PageMetadata | None = None, key: str = '') -> Dict:
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
    @classmethod
    @abstractmethod
    def model(cls) -> DefaultMeta:
        pass

    @property
    @classmethod
    @abstractmethod
    def response_schema(cls) -> Type[BaseModel]:
        pass

    @property
    def post_schema(cls) -> Type[BaseModel]:
        return cls.response_schema

    @property
    def patch_schema(cls) -> Type[BaseModel]:
        return cls.response_schema

    @property
    def update_schema(cls) -> Type[BaseModel]:
        return cls.response_schema

    @classmethod
    def get(cls, query: Dict = None):
        """Fetch objects from storage."""
        query = Repository.get_all(cls.model)
        response = cls.paginate(query=query, serializer=cls.response_schema,
                                meta_data=cls.pagination)
        return jsonify(response)

    @classmethod
    def post(cls, parameters: Optional[Dict] = None, 
             query: Optional[Dict] = None,
             data: Type[BaseModel] = None):
        """Create new object and add to storage."""
        # Validate incoming request and deserilize into pydantic model
        # try:
        data: Type[BaseModel] = cls.post_schema(**request.json)
        # except ValidationError as exc:
        #     errors = exc.errors()
        #     for error in errors:
        #         del error['input']
        #         if error.get('url'):
        #             del error['url']

        #     return jsonify(errors), 422

        # serialize into dictionary and load data into database
        model = data.model_dump()
        obj = cls.model().save(**model)

        # Serialize response for frontend.
        response = cls.response_schema.model_validate(obj).model_dump()
        return jsonify(response), 201


class DetailView(BaseView):
    """Get, Update or Delete an object in storage."""
    @classmethod
    def get(cls: Type[Base], id: int):
        """Get specif object from storage."""
        obj = Repository.get_one(cls.model, oid=id)
        serialized_item = cls.response_schema.model_validate(obj)
        response = {'data': serialized_item.model_dump()}
        return jsonify(response)

    @classmethod
    def put(cls, id: int):
        """Update all values to new data."""
        obj = Repository.get_one(cls.model, oid=id)

        # Validate, deserialize input data into pydantic model
        # and then dump it as dict.
        post_data = request.json
        cls.update_schema.model_validate(post_data, strict=True)

        # Get all public attributes of model updated.
        obj.update(obj=obj, data=post_data)
        return '', 204

    @classmethod
    def patch(cls, id: int):
        """Update object in storage partially."""
        obj = Repository.get_one(cls.model, oid=id)

        # Validate, deserialize input data into pydantic model
        # and then dump it as dict.
        patch_data = request.json
        cls.patch_schema.model_validate(patch_data, strict=True)
        obj = obj.update(obj=obj, data=patch_data)

        # Deserialize model object.
        serialized_obj = cls.response_schema.model_validate(obj).model_dump()
        response = {'data': serialized_obj}
        return jsonify(response)

    @classmethod
    def delete(cls, id: int, permanent: bool = False):
        """Delete object from storage."""
        permanent = request.args.get(
            'permanent', False,
            type=lambda x: bool(1 if x.lower() == 'true' else 0))

        obj = Repository.get_one(cls.model, oid=id)
        cls.model.delete(obj=obj, permanent=permanent)
        return '', 204
