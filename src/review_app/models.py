import pydantic


# User --------------------------------------------------------------------------------------------
class UserBase(pydantic.BaseModel):
    name: str
    age: int | None


class UserCreate(UserBase):
    pass


class User(UserBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    # reviews: list['Review'] = []


# MediaType --------------------------------------------------------------------
class MediaTypeBase(pydantic.BaseModel):
    name: str


class MediaTypeCreate(MediaTypeBase):
    pass


class MediaType(MediaTypeBase):
    model_config = pydantic.ConfigDict(from_attributes=True)
    id: int


# Author -----------------------------------------------------------------------
class AuthorBase(pydantic.BaseModel):
    name: str
    alive: bool


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int


# Media ------------------------------------------------------------------------
class MediaBase(pydantic.BaseModel):
    title: str
    media_type_id: int
    author_id: int | None


class MediaCreate(MediaBase):
    pass


class Media(MediaBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    media_type: MediaType
    author: Author | None


# Review -----------------------------------------------------------------------
class ReviewBase(pydantic.BaseModel):
    media_id: int
    user_id: int
    rating: int
    review: str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    model_config = pydantic.ConfigDict(from_attributes=True)

    id: int
    media: Media
    user: User
