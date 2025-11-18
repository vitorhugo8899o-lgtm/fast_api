from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.models import Product, User
from fast_api.expections.expect import (
    ProductNotFound,
    UserNotAdm,
    UserNotFound,
)
from fast_api.Schemas.Schema import (
    OrderRequest,
    ProductSchema,
)


async def found_user_adm(db: AsyncSession, user_data: User) -> bool:

    user_search = await db.scalar(select(User).where(User.id == user_data.id))

    if not user_search:
        raise UserNotFound

    if not user_search.adm:
        raise UserNotAdm

    return True


async def add_products(db: AsyncSession, product: ProductSchema):

    new_product = Product(
        type=product.type,
        name=product.name,
        price=product.price,
        collor=product.collor,
        stock=product.stock,
        size=product.size,
    )

    db.add(new_product)
    await db.commit()


async def search_product_delete(db: AsyncSession, product):
    product = await db.scalar(
        select(Product).where(Product.id_product == product.id)
    )

    if product is None:
        raise ProductNotFound

    await db.delete(product)
    await db.commit()


async def search_for_product(db: AsyncSession, product: OrderRequest):
    stmt = (
        select(Product)
        .filter(Product.id_product == product.id_product)
        .limit(1)
    )

    product_found = await db.scalar(stmt)

    if product_found is None:
        raise ProductNotFound

    return product_found
