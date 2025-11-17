from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.Depends import create_session
from fast_api.database.models import Order, User
from fast_api.expections.expect import OrderNotFound, ProductNotFound
from fast_api.Schemas.Schema import (
    Message,
    MessageOrder,
    OrderList,
    OrderRequest,
)
from fast_api.services.master_services import search_for_product
from fast_api.services.user_services import get_current_user, search_for_order

routh_order = APIRouter(prefix='/order', tags=['Orders'])
Db = Annotated[AsyncSession, Depends(create_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@routh_order.post(
    '/place_order', status_code=HTTPStatus.CREATED, response_model=MessageOrder
)
async def place_order(
    db: Db, current_user: CurrentUser, product: OrderRequest
):

    query = await search_for_product(db=db, product=product)

    if not query:
        raise ProductNotFound

    order = Order(
        id_product=query.id_product,
        user_id=current_user.id,
        total_amount=query.price,
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    return MessageOrder(
        message='Order completed',
        id=order.id_order,
        id_product=order.id_product,
        id_user=order.user_id,
        total_amount=order.total_amount,
        created_at=order.created_at,
    )


@routh_order.get(
    '/show_orders', status_code=HTTPStatus.OK, response_model=OrderList
)
async def get_orders_by_user(db: Db, current_user: CurrentUser):
    return {'orders': current_user.orders}


@routh_order.delete('/cancel_order', response_model=Message)
async def delete_order(db: Db, current_user: CurrentUser, id_order: int):

    query = await search_for_order(db=db, order=id_order)

    if not query:
        raise OrderNotFound

    if query.user_id != current_user.id:
        raise OrderNotFound

    await db.delete(query)
    await db.commit()

    return Message(message='Order successfully cancelled')
