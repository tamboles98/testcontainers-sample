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


def test_get_user(minimal_initiated_database: 'DatabaseItems', database_session: 'Session'):
    user = minimal_initiated_database.users[0]
    db_service = DatabaseService(database_session)
    res_user = db_service.get_user(user_id=user.id)
    user.name == res_user.name


def test_get_missing_user(database_session: 'Session'):
    db_service = DatabaseService(database_session)
    with pytest.raises(NotFoundError):
        db_service.get_user(user_id=1)
