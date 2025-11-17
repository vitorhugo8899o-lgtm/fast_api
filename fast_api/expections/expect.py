from http import HTTPStatus

from fastapi import HTTPException


class GenericServerError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail='Internal server error!',
        )


class EmailAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='This email address is already in use.',
        )


class UserNameAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='Username is already in use.',
        )


class InvalidCredentialsErrorLogin(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password.',
        )


class TokenDecodeError(HTTPException):
    def __init__(self):
        super().__init__(
            HTTPStatus.UNAUTHORIZED, detail='Invalid token error!'
        )


class TokenExpireError(HTTPException):
    def __init__(self):
        super().__init__(
            HTTPStatus.UNAUTHORIZED,
            detail='Token expired, please log in again.',
        )


class InvalidCredentials(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid credentials!',
            headers={'WWW-Authenticate': 'Bearer'},
        )


class WithoutSufficientAuthorization(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You are not permitted to perform this activity',
        )


class IntegrityErrorUser(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='Email or username already in use.',
        )


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found!',
        )


class UserNotAdm(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='The user is not an administrator.',
        )


class ProductAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='The product already registered.',
        )


class ProductAlreadyInStock(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='The product already in stock.',
        )


class ProductNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='The product was not found.',
        )


class OrderNotFound(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.CONFLICT,
            detail='The order was not found.',
        )
