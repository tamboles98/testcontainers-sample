"""Tests for the main module with fastapi application logic.

Most of the functions are simple wrappers around the database service, so we will
create fixtures that mock different behaviours of the database service. Each fixture
maps to a method in the database service and is parametrized to simulate all the possible
outcomes of the method. All fixtures return the a MockedResult object that contains the
status of the mock, the result, the error (if any), and a description of the behaviour.
The tests will use these fixtures to test the different behaviours of the main module."""

import typing as ty
from dataclasses import dataclass
from enum import Enum
from unittest.mock import MagicMock, create_autospec

import pytest

import review_app.main as main
from review_app import schemas
from review_app.database import service


class MockStatus(Enum):
    """Enum to represent the status of a mocked function so we can handle different
    behaviours in the tests.
    """

    SUCCESS = 'success'  # Normal behaviour, no error
    DYNAMIC = 'dynamic'  # Dynamic behaviour, no error
    EMPTY = 'empty'  # Empty result, no error
    ERROR = 'error'


@dataclass
class MockedResult:
    status: MockStatus
    result: ty.Any = None
    error: ty.Optional[Exception] = None
    mock_function: ty.Optional[ty.Callable[..., ty.Any]] = None
    description: str = ''


@pytest.fixture
def mock_db_service():
    database_service = create_autospec(service.DatabaseService, instance=True)
    return database_service


@pytest.fixture
def patch_db_create_user(mock_db_service: MagicMock):
    def create_user(user: schemas.UserCreate) -> schemas.User:
        return schemas.User(id=1, **user.model_dump())

    mock_db_service.create_user = create_user
    return MockedResult(status=MockStatus.DYNAMIC, mock_function=create_user)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_user(request, mock_db_service: service.DatabaseService):
    if request.param == 'success':
        get_user = schemas.User(id=1, name='John Doe', age=25)
        mock_db_service.get_user.return_value = get_user
        return MockedResult(status=MockStatus.SUCCESS, result=get_user)
    else:
        error = service.NotFoundError('User not found')
        mock_db_service.get_user.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error)


# Tests -----------------------------------------------------------------------
# User ------------------------------------------------------------------------
@pytest.fixture(params=['success', 'empty', 'not_found'])
def patch_db_get_user_reviews(request: ty.Any, mock_db_service: MagicMock):
    if request.param == 'success':
        user = schemas.User(id=1, name='John Doe', age=25)
        media_type = schemas.MediaType(id=1, name='Game')
        author = schemas.Author(id=1, name='Nintendo', alive=True)
        media = schemas.Media(id=1, title='Pokemon', media_type_id=1, author_id=1, media_type=media_type, author=author)
        get_user_reviews = [
            schemas.Review(id=1, media_id=1, user_id=1, rating=3, review='Too much water', media=media, user=user)
        ]
        mock_db_service.get_user_reviews.return_value = get_user_reviews
        return MockedResult(status=MockStatus.SUCCESS, result=get_user_reviews, description='User has reviews')
    elif request.param == 'empty':
        result = []
        mock_db_service.get_user_reviews.return_value = result
        return MockedResult(status=MockStatus.EMPTY, result=result, description='User has no reviews')
    else:
        error = service.NotFoundError('User not found')
        mock_db_service.get_user_reviews.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error, description='User not found')


def test_create_user(mock_db_service: MagicMock, patch_db_create_user: MockedResult):
    user = schemas.UserCreate(name='John Doe', age=25)
    created_user = main.create_user(user, db=mock_db_service)
    assert isinstance(created_user.id, int)
    assert created_user.name == 'John Doe'
    assert created_user.age == 25


def test_read_user(mock_db_service: MagicMock, patch_db_get_user: MockedResult):
    if patch_db_get_user.status == MockStatus.SUCCESS:
        user = main.read_user(1, db=mock_db_service)
        assert user.id == 1
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_user(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


def test_read_user_reviews(mock_db_service: MagicMock, patch_db_get_user_reviews: MockedResult):
    if patch_db_get_user_reviews.status == MockStatus.SUCCESS:
        reviews = main.read_user_reviews(1, db=mock_db_service)
        assert len(reviews) == 1
        assert all(isinstance(review, schemas.Review) for review in reviews)
    elif patch_db_get_user_reviews.status == MockStatus.EMPTY:
        reviews = main.read_user_reviews(1, db=mock_db_service)
        assert len(reviews) == 0
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_user_reviews(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


# MediaType --------------------------------------------------------------------
@pytest.fixture
def patch_db_create_media_type(mock_db_service: MagicMock):
    def create_media_type(media_type: schemas.MediaTypeCreate) -> schemas.MediaType:
        return schemas.MediaType(id=1, **media_type.model_dump())

    mock_db_service.create_media_type = create_media_type
    return MockedResult(status=MockStatus.DYNAMIC, mock_function=create_media_type)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_media_type(request: ty.Any, mock_db_service: MagicMock):
    if request.param == 'success':
        get_media_type = schemas.MediaType(id=1, name='Movie')
        mock_db_service.get_media_type.return_value = get_media_type
        return MockedResult(status=MockStatus.SUCCESS, result=get_media_type)
    else:
        error = service.NotFoundError('Media type not found')
        mock_db_service.get_media_type.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error)


def test_create_media_type(mock_db_service: MagicMock, patch_db_create_media_type: MockedResult):
    media_type = schemas.MediaTypeCreate(name='Movie')
    created_media_type = main.create_media_type(media_type, db=mock_db_service)
    assert isinstance(created_media_type.id, int)
    assert created_media_type.name == 'Movie'


def test_read_media_type(mock_db_service: MagicMock, patch_db_get_media_type: MockedResult):
    if patch_db_get_media_type.status == MockStatus.SUCCESS:
        media_type = main.read_media_type(1, db=mock_db_service)
        assert media_type.id == 1
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_media_type(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


# Media ----------------------------------------------------------------------
@pytest.fixture
def patch_db_create_media(mock_db_service: MagicMock):
    def create_media(media: schemas.MediaCreate) -> schemas.Media:
        media_type = schemas.MediaType(id=media.media_type_id, name='Game')
        author = schemas.Author(id=media.author_id, name='Nintendo', alive=True)
        return schemas.Media(id=1, media_type=media_type, author=author, **media.model_dump())

    mock_db_service.create_media = create_media
    return MockedResult(status=MockStatus.DYNAMIC, mock_function=create_media)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_media(request, mock_db_service: service.DatabaseService):
    if request.param == 'success':
        get_media = schemas.Media(
            id=1,
            title='Test Media',
            media_type_id=1,
            author_id=1,
            media_type=schemas.MediaType(id=1, name='Test Type'),
            author=schemas.Author(id=1, name='Test Author', alive=True),
        )
        mock_db_service.get_media.return_value = get_media
        return MockedResult(status=MockStatus.SUCCESS, result=get_media)
    else:
        error = service.NotFoundError('Media not found')
        mock_db_service.get_media.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error)


def test_create_media(mock_db_service: MagicMock, patch_db_create_media: MockedResult):
    media = schemas.MediaCreate(title='Test Media', media_type_id=1, author_id=1)
    created_media = main.create_media(media, db=mock_db_service)
    assert isinstance(created_media.id, int)
    assert created_media.title == 'Test Media'
    assert created_media.media_type_id == 1
    assert created_media.author_id == 1


def test_read_media(mock_db_service: MagicMock, patch_db_get_media: MockedResult):
    if patch_db_get_media.status == MockStatus.SUCCESS:
        media = main.read_media(1, db=mock_db_service)
        assert media.id == 1
        assert media.title == 'Test Media'
        assert media.media_type_id == 1
        assert media.author_id == 1
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_media(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


# Reviews ---------------------------------------------------------------------
@pytest.fixture
def patch_db_create_review(mock_db_service: MagicMock):
    def create_review(review: schemas.ReviewCreate) -> schemas.Review:
        media_type = schemas.MediaType(id=1, name='Game')
        author = schemas.Author(id=1, name='Nintendo', alive=True)
        media = schemas.Media(
            id=review.media_id, title='Test Media', media_type_id=1, author_id=1, author=author, media_type=media_type
        )
        user = schemas.User(id=review.user_id, name='John Doe', age=25)
        return schemas.Review(id=1, media=media, user=user, **review.model_dump())

    mock_db_service.create_review = create_review
    return MockedResult(status=MockStatus.DYNAMIC, mock_function=create_review)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_review(request, mock_db_service: service.DatabaseService):
    if request.param == 'success':
        media_type = schemas.MediaType(id=1, name='Game')
        author = schemas.Author(id=1, name='Nintendo', alive=True)
        get_review = schemas.Review(
            id=1,
            media_id=1,
            user_id=1,
            rating=5,
            review='Great movie',
            media=schemas.Media(
                id=1, title='Test Media', media_type_id=1, author_id=1, media_type=media_type, author=author
            ),
            user=schemas.User(id=1, name='John Doe', age=25),
        )
        mock_db_service.get_review.return_value = get_review
        return MockedResult(status=MockStatus.SUCCESS, result=get_review)
    else:
        error = service.NotFoundError('Review not found')
        mock_db_service.get_review.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error)


def test_create_review(mock_db_service: MagicMock, patch_db_create_review: MockedResult):
    review = schemas.ReviewCreate(media_id=1, user_id=1, rating=5, review='Great movie')
    created_review = main.create_review(review, db=mock_db_service)
    assert isinstance(created_review.id, int)
    assert created_review.media_id == 1
    assert created_review.user_id == 1
    assert created_review.rating == 5
    assert created_review.review == 'Great movie'


def test_read_review(mock_db_service: MagicMock, patch_db_get_review: MockedResult):
    if patch_db_get_review.status == MockStatus.SUCCESS:
        review = main.read_review(1, db=mock_db_service)
        assert review.id == 1
        assert review.media_id == 1
        assert review.user_id == 1
        assert review.rating == 5
        assert review.review == 'Great movie'
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_review(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


# Author ---------------------------------------------------------------------
@pytest.fixture
def patch_db_create_author(mock_db_service: MagicMock):
    def create_author(author: schemas.AuthorCreate) -> schemas.Author:
        return schemas.Author(id=1, **author.model_dump())

    mock_db_service.create_author = create_author
    return MockedResult(status=MockStatus.DYNAMIC, mock_function=create_author)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_author(request: ty.Any, mock_db_service: MagicMock):
    if request.param == 'success':
        get_author = schemas.Author(id=1, name='Test Author', alive=True)
        mock_db_service.get_author.return_value = get_author
        return MockedResult(status=MockStatus.SUCCESS, result=get_author)
    else:
        error = service.NotFoundError('Author not found')
        mock_db_service.get_author.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error)


@pytest.fixture(params=['success', 'not_found'])
def patch_db_get_author_highest_rated_media(request: ty.Any, mock_db_service: MagicMock):
    if request.param == 'success':
        author = schemas.Author(id=1, name='Test Author', alive=True)
        media_type = schemas.MediaType(id=1, name='Game')
        media = schemas.Media(
            id=1, title='Test Media', media_type_id=1, author_id=1, author=author, media_type=media_type
        )
        get_author_highest_rated_media = media
        mock_db_service.get_author_highest_rated_media.return_value = get_author_highest_rated_media
        return MockedResult(
            status=MockStatus.SUCCESS,
            result=get_author_highest_rated_media,
            description='Author has highest rated media',
        )
    else:
        error = service.NotFoundError('Author not found')
        mock_db_service.get_author_highest_rated_media.side_effect = error
        return MockedResult(status=MockStatus.ERROR, error=error, description='Author not found')


def test_create_author(mock_db_service: MagicMock, patch_db_create_author: MockedResult):
    author = schemas.AuthorCreate(name='Test Author', alive=True)
    created_author = main.create_author(author, db=mock_db_service)
    assert isinstance(created_author.id, int)
    assert created_author.name == 'Test Author'
    assert created_author.alive is True


def test_read_author(mock_db_service: MagicMock, patch_db_get_author: MockedResult):
    if patch_db_get_author.status == MockStatus.SUCCESS:
        author = main.read_author(1, db=mock_db_service)
        assert author.id == 1
        assert author.name == 'Test Author'
        assert author.alive is True
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_author(1, db=mock_db_service)
            assert exc_info.value.status_code == 404


def test_read_author_highest_rated_media(
    mock_db_service: MagicMock, patch_db_get_author_highest_rated_media: MockedResult
):
    if patch_db_get_author_highest_rated_media.status == MockStatus.SUCCESS:
        media = main.read_author_highest_rated_media(1, db=mock_db_service)
        assert media.id == 1
        assert media.title == 'Test Media'
        assert media.media_type_id == 1
        assert media.author_id == 1
    else:
        with pytest.raises(main.HTTPException) as exc_info:
            main.read_author_highest_rated_media(1, db=mock_db_service)
            assert exc_info.value.status_code == 404
