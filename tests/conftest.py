from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from fast_api.app import app
from fast_api.database.Depends import create_session
from fast_api.database.models import User, mapper_registry
from fast_api.services.user_services import (
    hash_password,
)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[create_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(model, time=datetime(2025, 11, 11)):
    def fake_time_hook(mapper, connection, target):
        target.created_at = time
        print(target)

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest_asyncio.fixture
async def session():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        engine = create_async_engine(postgres.get_connection_url())

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.create_all)

        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session

        async with engine.begin() as conn:
            await conn.run_sync(mapper_registry.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(password=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def orther_user(session: AsyncSession):
    password = 'testtest'
    user = UserFactory(password=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = password

    return user


@pytest_asyncio.fixture
async def master_user(session: AsyncSession):
    password = 'master'
    master_user = User(
        username='master1',
        fullname='masterfull',
        email='master@gmail.com',
        password=hash_password(password),
        adm=True,
    )
    session.add(master_user)
    await session.commit()
    await session.refresh(master_user)

    master_user.clean_password = password

    return master_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/Login/',
        data={'username': user.email, 'password': 'tentacomedia'},
    )
    return response.json()['access_token']


@pytest.fixture
def token_master(client, master_user):
    response = client.post(
        '/auth/Login/',
        data={
            'username': master_user.email,
            'password': master_user.clean_password,
        },
    )
    return response.json()['access_token']


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    fullname = factory.Sequence(lambda n: f'testfull{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.Sequence(lambda n: f'@test{n}')


@pytest_asyncio.fixture
def test_register_product(client, token_master):

    product = {
        'type': 'cap',
        'name': 'Oakley',
        'price': 200,
        'collor': 'Red',
        'stock': True,
        'size': 'G',
    }

    response = client.post(
        '/master/register_product',
        headers={'Authorization': f'Bearer {token_master}'},
        json=product,
    )

    return response.json
