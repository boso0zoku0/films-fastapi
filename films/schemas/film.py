from typing import Annotated

from annotated_types import Len, MaxLen, MinLen
from pydantic import AnyHttpUrl, BaseModel

# Film_Annotated_description = Annotated[str, MaxLen(110)]
# Film_Annotated_slug = Annotated[str, MinLen(3), MaxLen(7)]
# DESCRIPTION_MAX_LENGTH = 110
Film_Annotated_slug = Annotated[str, Len(min_length=3, max_length=8)]
Film_Annotated_description = Annotated[str, MaxLen(300), MinLen(0)]
DESCRIPTION_MAX_LENGTH = 30
# class FilmsBase(BaseModel):
#     name: str
#     target_url: AnyHttpUrl
#     description: ShortAnnotated_description | None = ""
#     year_release: int
#
#
# class FilmsCreate(FilmsBase):
#
#     slug: ShortAnnotated_slug | None = ""
#
#
# class Films(FilmsBase):
#     notes: str = ""
#     slug: ShortAnnotated_slug | None = ""
#
#
# class FilmsRead(FilmsCreate):
#     slug: ShortAnnotated_slug | None = ""
#
#
# class FilmsUpdate(BaseModel):
#     name: str
#     target_url: AnyHttpUrl
#     description: ShortAnnotated_description | None = ""
#     year_release: int
#
#
# class FilmsUpdatePartial(BaseModel):
#     name: str | None = None
#     target_url: AnyHttpUrl | None = None
#     description: ShortAnnotated_description | None = None
#     year_release: int | None = None


class FilmsBase(BaseModel):
    name: str
    description: Film_Annotated_description
    year_release: int


class FilmsCreate(FilmsBase):
    slug: Film_Annotated_slug = ""


class Films(FilmsBase):
    notes: str = ""
    slug: Film_Annotated_slug | None = None


class FilmsRead(FilmsBase):
    slug: Film_Annotated_slug


class FilmsUpdate(BaseModel):
    name: str
    description: Film_Annotated_description
    year_release: int


class FilmsUpdatePartial(BaseModel):
    name: str | None = None
    description: Film_Annotated_description | None = None
    year_release: int | None = None
