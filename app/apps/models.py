from typing import Any, Union

from sqlalchemy import (
    JSON,
    Delete,
    MetaData,
    ScalarResult,
    Select,
    Update,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class BASE(DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_`%(constraint_name)s`",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%"
            "(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
    type_annotation_map = {dict[int | str, Any]: JSON}


class BaseModelMixin:
    @classmethod
    def _filter_field(
        cls,
        query: Union[Select[Any], Delete, Update],
        field_name: str,
        field_value: str | int | bool,
    ) -> Union[Select[Any], Delete, Update]:
        field_name, expr = field_name.split("__")
        if expr == "eq":
            query = query.where(getattr(cls, field_name) == field_value)
        elif expr == "ne":
            query = query.where(getattr(cls, field_name) != field_value)
        elif expr == "gt":
            query = query.where(getattr(cls, field_name) > field_value)
        elif expr == "ge":
            query = query.where(getattr(cls, field_name) >= field_value)
        elif expr == "lt":
            query = query.where(getattr(cls, field_name) < field_value)
        elif expr == "le":
            query = query.where(getattr(cls, field_name) <= field_value)
        else:
            query = query.where(getattr(cls, field_name) == field_value)
        return query

    @classmethod
    def filter(
        cls,
        query: Union[Select[Any], Delete, Update],
        filter_fields: dict,
    ) -> Union[Select[Any], Delete, Update]:
        for field, value in filter_fields.items():
            query = cls._filter_field(query, field, value)
        return query

    @classmethod
    async def select_query(
        cls, session: AsyncSession, filter_fields: dict | None = None
    ) -> ScalarResult[Any]:
        query: Select = select(cls)
        if filter_fields:
            query = cls.filter(query, filter_fields)  # type: ignore
        result = await session.execute(query)
        return result.scalars()

    @classmethod
    async def get_all(
        cls, session: AsyncSession, filter_fields: dict | None = None
    ) -> Any:
        return (await cls.select_query(session, filter_fields)).all()

    @classmethod
    async def get_first(
        cls, session: AsyncSession, filter_fields: dict | None = None
    ) -> Any:
        return (await cls.select_query(session, filter_fields)).first()
