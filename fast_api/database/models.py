from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

mapper_registry = registry()


@mapper_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    adm: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
    uptade_at: Mapped[datetime | None] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )

    orders: Mapped[list[Order]] = relationship(
        init=False, cascade='all, delete-orphan', lazy='selectin'
    )


@mapper_registry.mapped_as_dataclass
class Product:
    __tablename__ = 'products'

    id_product: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    collor: Mapped[str] = mapped_column(String(30), nullable=False)
    size: Mapped[str] = mapped_column(String(10), nullable=False)
    stock: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )


@mapper_registry.mapped_as_dataclass
class Order:
    __tablename__ = 'orders'

    id_order: Mapped[int] = mapped_column(
        Integer, init=False, primary_key=True, autoincrement=True
    )
    id_product: Mapped[int] = mapped_column(
        ForeignKey('products.id_product'), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    total_amount: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), nullable=False
    )
