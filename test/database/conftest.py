import os
import typing as ty

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from review_app.database.models import Author, Base, Media, MediaType, Review, User
from test.database.initializer_helper import DatabaseItems

if ty.TYPE_CHECKING:
    from sqlalchemy.engine import Engine

POSTGRES = PostgresContainer('postgres:16-alpine')


@pytest.fixture(scope='package', autouse=True)
def _database_setup(request) -> 'Engine':
    # setup code
    POSTGRES.start()

    def cleanup():
        os.environ.pop('DATABASE_URL')
        # teardown code
        POSTGRES.stop()

    request.addfinalizer(cleanup)

    database_url = POSTGRES.get_connection_url()
    os.environ['DATABASE_URL'] = database_url

    engine = create_engine(database_url)  # , connect_args={'check_same_thread': False}
    # Base.metadata.create_all(engine)

    return engine


@pytest.fixture(autouse=True)
def _wipe_database(_database_setup: 'Engine'):
    # This is inneficient, but it's the simplest way to clear the database
    Base.metadata.drop_all(_database_setup)
    Base.metadata.create_all(_database_setup)


@pytest.fixture
def database_session(_database_setup: 'Engine') -> ty.Generator[Session, None, None]:
    session = Session(_database_setup)

    yield session

    session.close()


@pytest.fixture
def minimal_initiated_database(database_session: Session) -> DatabaseItems:
    def create_objects() -> DatabaseItems:
        user = User(name='John Doe', age=25)
        media_type = MediaType(name='Book')
        author = Author(name='Jane Smith', alive=True)
        media = Media(title='The Great Gatsby', media_type=media_type, author=author)
        review = Review(media=media, user=user, rating=5, review='Great book!')

        return DatabaseItems(
            users=[user],
            media_types=[media_type],
            authors=[author],
            media=[media],
            reviews=[review],
        )

    objects = create_objects()
    database_session.add_all(objects.to_list())
    database_session.commit()
    return objects
