import pytest
from odmantic import ObjectId

from app.domain.entities import Pagination
from app.domain.entities import User
from app.domain.errors import PageNotFoundException
from tests.conftest import async_return


@pytest.fixture
def create_user_body():
    yield {
        'firebase_uid': '1234',
        'name': 'Test',
        'email': 'test@example.com',
    }


@pytest.fixture
def update_user_body():
    yield {
        'name': 'Test',
        'email': 'test@example.com',
        'permissions': ['test_1', 'test_2'],
    }


@pytest.mark.asyncio
class TestCreateUser:
    async def test_create_user_success(
        self,
        client,
        users_usecases_mock,
        create_user_body,
    ):
        user = User(**create_user_body)
        users_usecases_mock.create_user.return_value = async_return(user)

        response = client.post('/users/', json=create_user_body)

        assert response.json() == user.model_dump(mode='json')
        assert response.status_code == 201
        users_usecases_mock.create_user.assert_called_once()

    @pytest.mark.parametrize(
        'field,value',
        (
            ('firebase_uid', {}),
            ('email', {}),
            ('email', 'testexample.com'),
            ('email', 'test@example'),
            ('name', {}),
            ('permissions', {}),
        ),
    )
    async def test_create_user_wrong_fields(
        self,
        client,
        users_usecases_mock,
        create_user_body,
        field,
        value,
    ):
        create_user_body[field] = value

        response = client.post('/users/', json=create_user_body)

        assert response.status_code == 422
        users_usecases_mock.create_user.assert_not_called()

    @pytest.mark.parametrize(
        'field',
        (
            'firebase_uid',
            'email',
            'name',
        ),
    )
    async def test_create_user_missing_mandatory_fields(
        self,
        client,
        users_usecases_mock,
        create_user_body,
        field,
    ):
        create_user_body.pop(field)

        response = client.post('/users/', json=create_user_body)

        assert response.status_code == 422
        users_usecases_mock.create_user.assert_not_called()


@pytest.mark.asyncio
class TestListUsers:
    async def test_list_users_success(
        self,
        client,
        users_usecases_mock,
    ):
        entities = Pagination(
            count=1,
            next_page=None,
            page=0,
            page_size=1,
            entities=[
                User(
                    firebase_uid='1234',
                    name='Test',
                    email='test@example.com',
                    id=ObjectId('658f108412688c770b84b14a'),
                )
            ],
        )
        pagination = Pagination(count=1, next_page=None, page=0, page_size=10, entities=entities)

        users_usecases_mock.list_users.return_value = async_return(pagination)
        response = client.get('/users/', params={'page': 0, 'page_size': 10})

        assert response.json() == pagination.model_dump(mode='json')
        assert response.status_code == 200
        users_usecases_mock.list_users.assert_called_once()

    async def test_list_users_no_pages(
        self,
        client,
        users_usecases_mock,
    ):
        pagination = Pagination(count=1, next_page=None, page=0, page_size=10, entities=[])

        users_usecases_mock.list_users.return_value = async_return(pagination)
        response = client.get('/users/', params={'page': 0, 'page_size': 10})

        assert response.json() == pagination.model_dump(mode='json')
        assert response.status_code == 200
        users_usecases_mock.list_users.assert_called_once()

    async def test_list_users_wrong_page(
        self,
        client,
        users_usecases_mock,
    ):
        users_usecases_mock.list_users.side_effect = PageNotFoundException

        response = client.get('/users/')

        assert response.status_code == 404
        users_usecases_mock.list_users.assert_called_once()


@pytest.mark.asyncio
class TestGetUserByFirebaseUid:
    async def test_get_user_by_firebase_uid_success(
        self,
        client,
        users_usecases_mock,
    ):
        firebase_uid = '1234'
        user = User(
            firebase_uid=firebase_uid,
            name='Test',
            email='test@example.com',
            id=ObjectId('658f108412688c770b84b14a'),
        )
        users_usecases_mock.get_user_by_firebase_uid.return_value = async_return(user)

        response = client.get(f'/users/{firebase_uid}/')

        assert response.json() == user.model_dump(mode='json')
        assert response.status_code == 200
        users_usecases_mock.get_user_by_firebase_uid.assert_called_once()


@pytest.mark.asyncio
class TestUpdateUserByFirebaseUid:
    async def test_update_user_by_firebase_uid_success(
        self,
        client,
        users_usecases_mock,
        update_user_body,
    ):
        firebase_uid = '1234'
        user = User(firebase_uid=firebase_uid, **update_user_body)
        users_usecases_mock.update_user_by_firebase_uid.return_value = async_return(user)

        response = client.patch(f'/users/{firebase_uid}/', json=update_user_body)

        assert response.json() == user.model_dump(mode='json')
        assert response.status_code == 200
        users_usecases_mock.update_user_by_firebase_uid.assert_called_once()

    @pytest.mark.parametrize(
        'field,value',
        (
            ('email', {}),
            ('email', 'testexample.com'),
            ('email', 'test@example'),
            ('name', {}),
            ('permissions', {}),
        ),
    )
    async def test_update_user_by_firebase_uid_wrong_fields(
        self,
        client,
        users_usecases_mock,
        update_user_body,
        field,
        value,
    ):
        firebase_uid = '1234'
        update_user_body[field] = value

        response = client.patch(f'/users/{firebase_uid}/', json=update_user_body)

        assert response.status_code == 422
        users_usecases_mock.create_user.assert_not_called()


@pytest.mark.asyncio
class TestDeleteUserByFirebaseUid:
    async def test_delete_user_by_firebase_uid_success(
        self,
        client,
        users_usecases_mock,
    ):
        firebase_uid = '1234'
        user = User(
            firebase_uid=firebase_uid,
            name='Test',
            email='test@example.com',
            id=ObjectId('658f108412688c770b84b14a'),
        )
        users_usecases_mock.delete_user_by_firebase_uid.return_value = async_return(user)

        response = client.delete(f'/users/{firebase_uid}/')

        assert response.json() == user.model_dump(mode='json')
        assert response.status_code == 200
        users_usecases_mock.delete_user_by_firebase_uid.assert_called_once()
