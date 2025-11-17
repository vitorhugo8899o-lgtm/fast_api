from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.Depends import create_session
from fast_api.database.models import User
from fast_api.expections.expect import (
    InvalidCredentialsErrorLogin,
)
from fast_api.Schemas.Schema import (
    Token,
)
from fast_api.services.user_services import (
    crete_token_acesses,
    get_current_user,
    verify_password,
)

routh_auth = APIRouter(prefix='/auth', tags=['Authentication'])

Db = Annotated[AsyncSession, Depends(create_session)]
Form_data = Annotated[OAuth2PasswordRequestForm, Depends()]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routh_auth.post('/Login/', status_code=HTTPStatus.OK, response_model=Token)
async def login_with_acesses_token(
    db: Db,
    form_data: Form_data,
):

    user = await db.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user:
        raise InvalidCredentialsErrorLogin

    if not verify_password(user.password, form_data.password):
        raise InvalidCredentialsErrorLogin

    access_token = crete_token_acesses(data={'sub': user.email})

    return Token(access_token=access_token, token_type='Bearer')


@routh_auth.post('/refresh_token', response_model=Token)
async def refresh_access_token(user: CurrentUser):
    new_access_token = crete_token_acesses(data={'sub': user.email})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
