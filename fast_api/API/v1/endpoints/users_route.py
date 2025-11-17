from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.Depends import create_session
from fast_api.database.models import User
from fast_api.expections.expect import (
    IntegrityErrorUser,
    WithoutSufficientAuthorization,
)
from fast_api.Schemas.Schema import (
    FilterPage,
    FilterProduct,
    Message,
    ProductsList,
    UserList,
    UserPublic,
    UserRegistration,
)
from fast_api.services.user_services import (
    create_user,
    filter_products,
    get_current_user,
    hash_password,
)

routh_users = APIRouter(prefix='/user', tags=['Users'])
Db = Annotated[AsyncSession, Depends(create_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routh_users.post(
    '/Create_Account',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublic,
)
async def create_user_account(
    db: Db,
    user: UserRegistration,
):
    return await create_user(db=db, user_data=user)


@routh_users.get(
    '/users/',
    status_code=HTTPStatus.OK,
    response_model=UserList,
)
async def list_users(
    db: Db,
    current_user: CurrentUser,
    filter_page: Annotated[FilterPage, Query()],
):
    users = await db.scalars(
        select(User).limit(filter_page.limit).offset(filter_page.offset)
    )

    return {'users': users}


@routh_users.put('/alter/{user_id}', response_model=UserPublic)
async def change_information_user(
    db: Db,
    current_user: CurrentUser,
    user_id: int,
    user: UserRegistration,
):

    if current_user.id != user_id:
        raise WithoutSufficientAuthorization

    try:
        current_user.fullname = user.fullname
        current_user.username = user.username
        current_user.password = hash_password(user.password)
        current_user.email = user.email
        await db.commit()
        await db.refresh(current_user)

        return UserPublic(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
        )

    except IntegrityError:
        raise IntegrityErrorUser


@routh_users.delete('/users/{user_id}', response_model=Message)
async def delete_user(
    db: Db,
    current_user: CurrentUser,
    user_id: int,
):

    if current_user.id != user_id:
        raise WithoutSufficientAuthorization

    db.delete(current_user)
    await db.commit()

    return Message(message='User delete')


@routh_users.get(
    '/get_products', status_code=HTTPStatus.OK, response_model=ProductsList
)
async def list_products(
    db: Db, filter_product: Annotated[FilterProduct, Query()]
):

    query = await filter_products(db=db, filter_product=filter_product)

    return {'products': query}
