from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import review_app.database.models as sqlm  # sqlm = sql models
import review_app.models as pm  # pm = pydantic models
from review_app.database import database


class NotFoundError(Exception):
    pass


class DatabaseService:
    """Service class to interact with the database."""

    def __init__(self, session: Session):
        self.session = session

    @staticmethod
    def create_database_service() -> 'DatabaseService':
        return DatabaseService(database.SessionLocal())

    # User -----------------------------------------------------------------------
    def create_user(self, user: pm.UserCreate) -> pm.User:
        sql_user = sqlm.User(name=user.name, age=user.age)
        self.session.add(sql_user)
        self.session.commit()
        self.session.refresh(sql_user)
        return pm.User.model_validate(sql_user)

    def get_user(self, user_id: int) -> pm.User:
        sql_user = self.session.query(sqlm.User).get(user_id)
        if sql_user is None:
            raise NotFoundError(f'User with id {user_id} not found')
        return pm.User.model_validate(sql_user)

    def get_user_reviews(self, user_id: int) -> list[pm.Review]:
        sql_user = self.session.query(sqlm.User).get(user_id)
        if sql_user is None:
            raise NotFoundError(f'User with id {user_id} not found')
        return [pm.Review.model_validate(review) for review in sql_user.reviews]

    # Review ---------------------------------------------------------------------
    def create_review(self, review: pm.ReviewCreate) -> pm.Review:
        sql_review = sqlm.Review(
            media_id=review.media_id,
            user_id=review.user_id,
            rating=review.rating,
            review=review.review,
        )
        self.session.add(review)
        self.session.commit()
        return pm.Review.model_validate(sql_review)

    def get_review(self, review_id: int) -> pm.Review:
        sql_review = self.session.query(sqlm.Review).get(review_id)
        if sql_review is None:
            raise NotFoundError(f'Review with id {review_id} not found')
        return pm.Review.model_validate(sql_review)

    # Media ----------------------------------------------------------------------
    def create_media(self, media: pm.MediaCreate) -> pm.Media:
        sql_media = sqlm.Media(
            title=media.title,
            media_type_id=media.media_type_id,
            author_id=media.author_id,
        )
        self.session.add(sql_media)
        self.session.commit()
        return pm.Media.model_validate(sql_media)

    def get_media(self, media_id: int) -> pm.Media:
        sql_media = self.session.query(sqlm.Media).get(media_id)
        if sql_media is None:
            raise NotFoundError(f'Media with id {media_id} not found')
        return pm.Media.model_validate(sql_media)

    # MediaType ------------------------------------------------------------------
    def create_media_type(self, media_type: pm.MediaTypeCreate) -> pm.MediaType:
        sql_media_type = sqlm.MediaType(name=media_type.name)
        self.session.add(sql_media_type)
        self.session.commit()
        return pm.MediaType.model_validate(sql_media_type)

    def get_media_type(self, media_type_id: int) -> pm.MediaType:
        sql_media_type = self.session.query(sqlm.MediaType).get(media_type_id)
        if sql_media_type is None:
            raise NotFoundError(f'MediaType with id {media_type_id} not found')
        return pm.MediaType.model_validate(sql_media_type)

    def get_media_type_by_name(self, name: str) -> pm.MediaType:
        sql_media_type = (
            self.session.query(sqlm.MediaType).filter(sqlm.MediaType.name == name).first()
        )
        if sql_media_type is None:
            raise NotFoundError(f'MediaType with name {name} not found')
        return pm.MediaType.model_validate(sql_media_type)

    # Author ---------------------------------------------------------------------
    def create_author(self, author: pm.AuthorCreate) -> pm.Author:
        sql_author = sqlm.Author(name=author.name, alive=author.alive)
        self.session.add(sql_author)
        self.session.commit()
        return pm.Author.model_validate(sql_author)

    def get_author(self, author_id: int) -> pm.Author:
        sql_author = self.session.query(sqlm.Author).filter(sqlm.Author.id == author_id).first()
        if sql_author is None:
            raise NotFoundError(f'Author with id {author_id} not found')
        return pm.Author.model_validate(sql_author)

    def get_author_highest_rated_media(self, author_id: int) -> pm.Media:
        sql_media = (
            self.session.query(sqlm.Media)
            .join(sqlm.Review)
            .filter(sqlm.Media.author_id == author_id)
            .group_by(sqlm.Media.id)
            .order_by(func.avg(sqlm.Review.rating).desc())
            .first()
        )
        if sql_media is None:
            raise NotFoundError(f'No media found for author with id {author_id}')
        return pm.Media.model_validate(sql_media)
