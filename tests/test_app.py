from http import HTTPStatus

import pytest
from freezegun import freeze_time


def test_home(client):

    response = client.get('/')

    status_code = 200

    assert response.status_code == status_code
    assert response.json() == {'message': 'E-commerce API no ar!'}


@pytest.mark.asyncio
async def test_get_token(client, user):
    response = client.post(
        '/auth/Login/',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_token_expired_after_time(client, user):
    with freeze_time('2018-10-31 12:00:00'):
        response = client.post(
            '/auth/Login',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.put(
            f'/user/alter/{user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'fullname': 'wrong da silva',
                'username': 'wrongwrong',
                'email': 'wrong@wrong.com',
                'password': 'wrong',
            },
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {
            'detail': 'Token expired, please log in again.'
        }


def test_uptade_user_erro(client, orther_user, token):
    response = client.put(
        f'/user/alter/{orther_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'trocado',
            'fullname': 'banana sama',
            'email': 'marceco@gmail.com',
            'password': 'string',
        },
    )
    assert response.json() == {
        'detail': 'You are not permitted to perform this activity'
    }
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user_erro(client, orther_user, token):
    response = client.delete(
        f'/user/users/{orther_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You are not permitted to perform this activity'
    }


def test_password_login_erro(client, user):
    response = client.post(
        '/auth/Login/',
        data={'username': user.email, 'password': 'bhsncxj2123'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password.'}


def test_email_login_erro(client, user):
    response = client.post(
        '/auth/Login/',
        data={'username': 'mamaco@gmail.com', 'password': user.password},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password.'}


def test_get_users(client, user, token):
    response = client.get(
        '/user/users/',
        headers={
            'Authorization': f'Bearer {token}',
            'filter_page.limit': '5',
            'filter_page.offset': '0',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert 'users' in response.json()


def test_alter_user(client, user, token):
    via_body = {
        'username': 'mauqicosilva7',
        'fullname': 'nomefull',
        'email': 'maca@email.com',
        'password': 'string',
    }

    response = client.put(
        f'/user/alter/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=via_body,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'mauqicosilva7'


def test_delete_user(client, user, token):
    response = client.delete(
        f'/user/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['message'] == 'User delete'
