# ruff: noqa: B008
from fastapi import Depends, FastAPI, HTTPException

from . import schemas
from .database import service

app = FastAPI()


# User -----------------------------------------------------------------------
@app.post('/users/', response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.User:
    return db.create_user(user=user)


@app.get('/users/{user_id}', response_model=schemas.User)
def read_user(user_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)):
    try:
        user = db.get_user(user_id=user_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='User not found') from e
    return user


@app.get('/users/{user_id}/reviews', response_model=list[schemas.Review])
def read_user_reviews(
    user_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> list[schemas.Review]:
    try:
        reviews = db.get_user_reviews(user_id=user_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='User not found') from e
    return reviews


# MediaType --------------------------------------------------------------------
@app.post('/media_types/', response_model=schemas.MediaType)
def create_media_type(
    media_type: schemas.MediaTypeCreate,
    db: service.DatabaseService = Depends(service.DatabaseService.create_database_service),
) -> schemas.MediaType:
    return db.create_media_type(media_type=media_type)


@app.get('/media_types/{media_type_id}', response_model=schemas.MediaType)
def read_media_type(
    media_type_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.MediaType:
    try:
        media_type = db.get_media_type(media_type_id=media_type_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='Media type not found') from e
    return media_type


# Review -----------------------------------------------------------------------
@app.post('/reviews/', response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.Review:
    return db.create_review(review=review)


@app.get('/reviews/{review_id}', response_model=schemas.Review)
def read_review(review_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)):
    try:
        review = db.get_review(review_id=review_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='Review not found') from e
    return review


# Media ----------------------------------------------------------------------
@app.post('/media/', response_model=schemas.Media)
def create_media(
    media: schemas.MediaCreate, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.Media:
    return db.create_media(media=media)


@app.get('/media/{media_id}', response_model=schemas.Media)
def read_media(media_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)):
    try:
        media = db.get_media(media_id=media_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='Media not found') from e
    return media


# Author ---------------------------------------------------------------------
@app.post('/authors/', response_model=schemas.Author)
def create_author(
    author: schemas.AuthorCreate, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.Author:
    return db.create_author(author=author)


@app.get('/authors/{author_id}', response_model=schemas.Author)
def read_author(author_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)):
    try:
        author = db.get_author(author_id=author_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='Author not found') from e
    return author


@app.get('/authors/{author_id}/highest_rated_media', response_model=schemas.Media)
def read_author_highest_rated_media(
    author_id: int, db: service.DatabaseService = Depends(service.DatabaseService.create_database_service)
) -> schemas.Media:
    try:
        media = db.get_author_highest_rated_media(author_id=author_id)
    except service.NotFoundError as e:
        raise HTTPException(status_code=404, detail='Author not found') from e
    return media
