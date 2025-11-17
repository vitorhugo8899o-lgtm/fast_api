from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.database.models import Product, User
from fast_api.expections.expect import (
    EmailAlreadyExistsError,
    ProductNotFound,
    UserNameAlreadyExistsError,
    UserNotAdm,
    UserNotFound,
)
from fast_api.Schemas.Schema import (
    OrderRequest,
    ProductSchema,
    UserAdm,
)
from fast_api.services.user_services import hash_password


async def create_adm(db: AsyncSession, user_data: UserAdm) -> User:

    condition = (User.username == user_data.username) | (
        User.email == user_data.email
    )

    found_user = await db.scalar(select(User).where(condition))

    if found_user:
        if found_user.email == user_data.email:
            raise EmailAlreadyExistsError
        elif found_user.username == user_data.username:
            raise UserNameAlreadyExistsError

    new_user = User(
        username=user_data.username,
        fullname=user_data.fullname,
        email=user_data.email,
        password=hash_password(user_data.password),
        adm=user_data.adm,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


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
