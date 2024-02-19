from abc import ABC
from typing import Optional

import pydantic


class AbstractTitle(pydantic.BaseModel, ABC):
    title: str
    description: str

    @pydantic.field_validator("title")
    @classmethod
    def title(cls, v: str) -> str:
        if len(v) < 30:
            raise ValueError(f"Maximum length of title is 30")
        return v

    @pydantic.field_validator("description")
    @classmethod
    def title(cls, v: str) -> str:
        if len(v) < 200:
            raise ValueError(f"Maximum length of description is 200")
        return v


class CreateAnn(AbstractTitle):
    title: str
    description: str


class UpdateAnn(AbstractTitle):
    title: Optional[str] = None
    description: Optional[str] = None
