from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from fast_api.Schemas.custom_schemas import PartnerBrands, Size, TypeProcuct


class Message(BaseModel):
    message: str


class UserRegistration(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str


class UserAdm(BaseModel):
    username: str
    fullname: str
    email: EmailStr
    password: str
    adm: bool


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: List[UserPublic]


class Userdelete(BaseModel):
    id: int
    username: str
    email: str


class Login(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = Field(ge=0, default=0)
    limit: int = Field(ge=0, default=0)


class FilterProduct(FilterPage):
    name: str | None = Field(default=None, min_length=4)
    type: str | None = Field(default=None, min_length=3)
    price: float | None = Field(default=None)
    collor: str | None = Field(default=None, min_length=3)
    size: str | None = Field(default=None, max_length=3)
    stock: bool | None = Field(default=True)


class ProductSchema(BaseModel):
    type: TypeProcuct
    name: PartnerBrands
    price: float
    collor: str
    stock: bool
    size: Size


class ProductPublic(ProductSchema):
    id_product: int

    model_config = ConfigDict(from_attributes=True)


class ProductsList(BaseModel):
    products: List[ProductPublic]


class AlterProduct(ProductSchema):
    id: int


class MessageOrder(Message):
    id: int
    id_product: int
    id_user: int
    total_amount: float
    created_at: datetime


class OrderSchema(BaseModel):
    id_order: int
    id_product: int
    id_user: int = Field(alias='user_id')
    total_amount: float = Field(alias='total_amount')
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class OrderRequest(BaseModel):
    id_product: int


class OrderList(BaseModel):
    orders: List[OrderSchema]


class OrderDelete(BaseModel):
    id_order: int
