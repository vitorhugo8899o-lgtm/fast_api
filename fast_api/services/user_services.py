from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import DecodeError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_api.core.settings import Settings
from fast_api.database.Depends import create_session
from fast_api.database.models import Order, Product, User
from fast_api.expections.expect import (
    EmailAlreadyExistsError,
    GenericServerError,
    InvalidCredentials,
    OrderNotFound,
    TokenDecodeError,
    TokenExpireError,
    UserNameAlreadyExistsError,
)
from fast_api.Schemas.Schema import (
    FilterProduct,
    OrderDelete,
    UserRegistration,
)

oauth2 = OAuth2PasswordBearer(tokenUrl='/auth/Login/')
setting = Settings()


def hash_password(password: str) -> str:
    """
    encrypt the password
    """
    ph = PasswordHasher()
    return ph.hash(password)


def verify_password(db_password: str, password: str) -> bool:
    """
    Take the raw password and encrypt
    it to see if it matches the password in the database.
    """
    ph = PasswordHasher()

    try:
        ph.verify(hash=db_password, password=password)
        return True

    except VerificationError:
        return False

    except Exception:
        return False


async def create_user(db: AsyncSession, user_data: UserRegistration) -> User:
    """
    Creates the user in the database;
    if a user already exists with the same email or password,
    raises an exception.
    """

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
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


def crete_token_acesses(data: dict):
    """
    Create the access token.
    """
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=setting.ACESSES_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encode_jwt = encode(to_encode, setting.SECRET_KEY, setting.ALGORITHM)
    return encode_jwt


async def get_current_user(
    token: str = Depends(oauth2), db: AsyncSession = Depends(create_session)
):
    """
    Retrieves the logged-in user's token and decodes it,
    retrieving the sub attribute; if it doesn't exist, it returns an error.
    """

    try:
        payload = decode(
            token, setting.SECRET_KEY, algorithms=setting.ALGORITHM
        )
        get_email = payload.get('sub')
        if not get_email:
            raise InvalidCredentials

    except DecodeError:
        raise TokenDecodeError

    except ExpiredSignatureError:
        raise TokenExpireError

    except Exception:
        raise GenericServerError

    user = await db.scalar(select(User).where(User.email == get_email))

    if not user:
        raise InvalidCredentials

    return user


async def filter_products(db: AsyncSession, filter_product: FilterProduct):
    """
    function to apply the search filter to the products
    """

    query = select(Product)

    contains_fields = ['type', 'name', 'price', 'collor', 'size']

    filter_data = filter_product.model_dump(
        exclude={'limit', 'offset', 'stock'}
    )

    for field, value in filter_data.items():
        if value is not None and field in contains_fields:
            db_attribute = getattr(Product, field)
            query = query.filter(db_attribute.contains(value))

    if filter_product.stock is not None:
        query = query.filter(Product.stock == filter_product.stock)

    query = query.limit(filter_product.limit).offset(filter_product.offset)

    product = await db.scalars(query)

    return product


async def search_for_order(db: AsyncSession, order: OrderDelete):
    """
    It searches the Orders table and returns the order
    if it doesn't find it, it throws an exception.
    """
    stmt = select(Order).filter(Order.id_order == order)

    order_found = await db.scalar(stmt)

    if order_found is None:
        raise OrderNotFound

    return order_found
