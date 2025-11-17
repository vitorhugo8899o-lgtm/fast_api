from http import HTTPStatus

import pytest
from jwt import decode

from fast_api.services.user_services import crete_token_acesses, setting


def test_jwt():
    data = {'test': 'test'}

    token = crete_token_acesses(data)

    decoded = decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


@pytest.mark.asyncio
async def test_jwt_invalid_token(client):

    response = client.delete(
        '/user/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid token error!'}


def test_refresh_token(client, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    json = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert 'token_type' in response.json()
    assert json['token_type'] == 'bearer'
