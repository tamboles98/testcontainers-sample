import pydantic


# User --------------------------------------------------------------------------------------------
class UserBase(pydantic.BaseModel):
    name: str
    age: int | None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    reviews : list['Review'] = []

    class Config:
        orm_mode = True

# MediaType --------------------------------------------------------------------
class MediaTypeBase(pydantic.BaseModel):
    name: str

class MediaTypeCreate(MediaTypeBase):
    pass

class MediaType(MediaTypeBase):
    id: int

    class Config:
        orm_mode = True

# Author -----------------------------------------------------------------------
class AuthorBase(pydantic.BaseModel):
    name: str
    alive: bool

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# Media ------------------------------------------------------------------------
class MediaBase(pydantic.BaseModel):
    title: str
    media_type_id: int
    author_id: int | None

class MediaCreate(MediaBase):
    pass

class Media(MediaBase):
    id: int
    media_type: MediaType
    author: Author | None

    class Config:
        orm_mode = True

# Review -----------------------------------------------------------------------
class ReviewBase(pydantic.BaseModel):
    media_id: int
    user_id: int
    rating: int
    review: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    media: Media
    user: User

    class Config:
        orm_mode = True