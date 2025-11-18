from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.Depends import create_session
from fast_api.database.models import User
from fast_api.expections.expect import (
    WithoutSufficientAuthorization,
)
from fast_api.Schemas.Schema import (
    Message,
    ProductSchema,
)
from fast_api.services.master_services import (
    add_products,
    found_user_adm,
    search_product_delete,
)
from fast_api.services.user_services import (
    get_current_user,
)

routh_master = APIRouter(prefix='/master', tags=['Adms'])
Db = Annotated[AsyncSession, Depends(create_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routh_master.post(
    '/register_product', status_code=HTTPStatus.CREATED, response_model=Message
)
async def register_products(
    db: Db, product: ProductSchema, current_user: CurrentUser
):

    user_search = await found_user_adm(db=db, user_data=current_user)
    if user_search:
        await add_products(db=db, product=product)

    return Message(message='Product successfully registered!')


@routh_master.delete(
    '/delete_product', status_code=HTTPStatus.OK, response_model=Message
)
async def delete_product(db: Db, current_user: CurrentUser, Product: int):

    user_search = await found_user_adm(db=db, user_data=current_user)

    if not user_search:
        raise WithoutSufficientAuthorization

    await search_product_delete(db=db, product=Product)

    return Message(message='Product successfully deleted!')
