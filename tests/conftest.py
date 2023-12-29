import asyncio
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.infrastructure.dependencies import users_usecases_dependency
from app.main import app


@pytest.fixture()
def users_usecases_mock():
    users_usecases = MagicMock()
    users_usecases.create_user = MagicMock()
    users_usecases.list_users = MagicMock()
    users_usecases.get_user_by_firebase_uid = MagicMock()
    users_usecases.update_user_by_firebase_uid = MagicMock()
    users_usecases.delete_user_by_firebase_uid = MagicMock()
    yield users_usecases


def async_return(result):
    f = asyncio.Future()
    f.set_result(result)
    return f


def dependency_mock(usecases_mock):
    async def func():
        return usecases_mock

    return func


@pytest.fixture()
def client(users_usecases_mock):
    client = TestClient(app)
    app.dependency_overrides[users_usecases_dependency] = dependency_mock(users_usecases_mock)
    yield client
