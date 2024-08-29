import typing as ty

import pytest

import review_app.models as pmodels
from review_app.database.service import DatabaseService, NotFoundError

if ty.TYPE_CHECKING:
    from sqlalchemy.orm import Session

    from test.database.initializer_helper import DatabaseItems


def test_save_user(database_session: 'Session'):
    db_service = DatabaseService(database_session)
    user = pmodels.UserCreate(name='John Doe', age=25)
    res_user = db_service.create_user(user)
    assert res_user.id is not None
    assert isinstance(res_user, pmodels.User)


def test_get_user(basic_database: 'DatabaseItems', database_session: 'Session'):
    user = basic_database.users[0]
    db_service = DatabaseService(database_session)
    res_user = db_service.get_user(user_id=user.id)
    assert user.name == res_user.name


def test_get_missing_user(empty_database: 'DatabaseItems', database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_user(user_id=1)


def test_get_user_reviews(basic_database: 'DatabaseItems', database_session: 'Session'):
    user = basic_database.users[0]
    db_service = DatabaseService(database_session)
    res_reviews = db_service.get_user_reviews(user_id=user.id)
    assert len(res_reviews) == 1
    assert all(isinstance(review, pmodels.Review) for review in res_reviews)


def test_get_user_reviews_missing_review(
    noreview_database: 'DatabaseItems', database_session: 'Session'
):
    user = noreview_database.users[0]
    db_service = DatabaseService(database_session)
    res_reviews = db_service.get_user_reviews(user_id=user.id)
    assert len(res_reviews) == 0


def test_get_user_reviews_missing_user(
    empty_database: 'DatabaseItems', database_session: 'Session'
):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_user_reviews(user_id=1)


def test_create_review(basic_database: 'DatabaseItems', database_session: 'Session'):
    user = basic_database.users[0]
    media = basic_database.media[0]
    review = pmodels.ReviewCreate(
        media_id=media.id, user_id=user.id, rating=3, review='Too much water'
    )
    db_service = DatabaseService(database_session)
    res_review = db_service.create_review(review)
    assert res_review.id is not None
    assert isinstance(res_review, pmodels.Review)


def test_get_review(basic_database: 'DatabaseItems', database_session: 'Session'):
    review = basic_database.reviews[0]
    db_service = DatabaseService(database_session)
    res_review = db_service.get_review(review_id=review.id)
    assert review.rating == res_review.rating


def test_get_missing_review(empty_database: 'DatabaseItems', database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_review(review_id=1)


def test_create_media(basic_database: 'DatabaseItems', database_session: 'Session'):
    media_type = basic_database.media_types[0]
    author = basic_database.authors[0]
    media = pmodels.MediaCreate(
        title='The Hobbit', media_type_id=media_type.id, author_id=author.id
    )
    db_service = DatabaseService(database_session)
    res_media = db_service.create_media(media)
    assert res_media.id is not None
    assert isinstance(res_media, pmodels.Media)


def test_get_media(basic_database: 'DatabaseItems', database_session: 'Session'):
    media = basic_database.media[0]
    db_service = DatabaseService(database_session)
    res_media = db_service.get_media(media_id=media.id)
    assert media.title == res_media.title


def test_get_missing_media(empty_database: 'DatabaseItems', database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_media(media_id=1)


def test_create_media_type(database_session: 'Session'):
    db_service = DatabaseService(database_session)
    media_type = pmodels.MediaTypeCreate(name='book')
    res_media_type = db_service.create_media_type(media_type)
    assert res_media_type.id is not None
    assert isinstance(res_media_type, pmodels.MediaType)


def test_get_media_type(basic_database: 'DatabaseItems', database_session: 'Session'):
    media_type = basic_database.media_types[0]
    db_service = DatabaseService(database_session)
    res_media_type = db_service.get_media_type(media_type_id=media_type.id)
    assert media_type.name == res_media_type.name


def test_get_missing_media_type(empty_database: 'DatabaseItems', database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_media_type(media_type_id=1)


def test_get_media_type_by_name(basic_database: 'DatabaseItems', database_session: 'Session'):
    media_type = basic_database.media_types[0]
    db_service = DatabaseService(database_session)
    res_media_type = db_service.get_media_type_by_name(media_type.name)
    assert media_type.id == res_media_type.id


def test_get_missing_media_type_by_name(
    empty_database: 'DatabaseItems', database_session: 'Session'
):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_media_type_by_name('book')


def test_create_author(database_session: 'Session'):
    db_service = DatabaseService(database_session)
    author = pmodels.AuthorCreate(name='J.R.R. Tolkien', alive=False)
    res_author = db_service.create_author(author)
    assert res_author.id is not None
    assert isinstance(res_author, pmodels.Author)


def test_get_author(basic_database: 'DatabaseItems', database_session: 'Session'):
    author = basic_database.authors[0]
    db_service = DatabaseService(database_session)
    res_author = db_service.get_author(author_id=author.id)
    assert author.name == res_author.name


def test_get_missing_author(empty_database: 'DatabaseItems', database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_author(author_id=1)


def test_get_author_highest_rated_media(
    rich_database: 'DatabaseItems', database_session: 'Session'
):
    author = rich_database.authors[1]  # J.R.R. Tolkien
    db_service = DatabaseService(database_session)
    res_media = db_service.get_author_highest_rated_media(author_id=author.id)
    # This should return the lord of the rings
    expected_media = rich_database.media[0]
    assert res_media.author_id == author.id
    assert res_media.title == expected_media.title
    assert res_media.media_type_id == expected_media.media_type_id


def test_get_author_highest_rated_media_no_review(
    noreview_database: 'DatabaseItems', database_session: 'Session'
):
    author = noreview_database.authors[0]
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_author_highest_rated_media(author_id=author.id)


def test_get_author_highest_rated_media_missing_author(
    empty_database: 'DatabaseItems', database_session: 'Session'
):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_author_highest_rated_media(author_id=1)


def test_get_author_highest_rated_media_no_media(
    nomedia_database: 'DatabaseItems', database_session: 'Session'
):
    author = nomedia_database.authors[0]
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_author_highest_rated_media(author_id=author.id)
