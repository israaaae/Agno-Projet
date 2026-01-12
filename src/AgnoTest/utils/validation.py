from __future__ import annotations

from typing import Any, Type, TypeVar

from pydantic import BaseModel

from exceptions import ValidationError

T = TypeVar("T", bound=BaseModel)


def validate_model(model_cls: Type[T], data: Any) -> T:
    try:
        if isinstance(data, model_cls):
            return data
        return model_cls.model_validate(data)
    except Exception as e:
        raise ValidationError(str(e)) from e


def dump_model(model: BaseModel) -> dict:
    return model.model_dump(mode="json")

