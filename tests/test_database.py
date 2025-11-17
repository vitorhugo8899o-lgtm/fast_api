from dataclasses import asdict

import pytest
from sqlalchemy import select

from fast_api.database.models import User


@pytest.mark.asyncio
async def test_user_model(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='testuser',
            email='vitor@gmail',
            password='securepassword',
            fullname='Vitor Silva',
            adm=False,
        )

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'testuser')
        )

    assert asdict(user) == {
        'adm': False,
        'id': user.id,
        'username': 'testuser',
        'email': 'vitor@gmail',
        'password': 'securepassword',
        'fullname': 'Vitor Silva',
        'created_at': time,
        'uptade_at': None,
        'orders': [],
    }
