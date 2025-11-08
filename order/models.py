from __future__ import annotations

import datetime
import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from order_system.db import Base

if TYPE_CHECKING:
    from product.models import ProductModel
    from user.models import UserModel

# Промежуточная таблица списка продуктов
product_in_order = Table(
    "products_in_order",
    Base.metadata,
    Column(
        "order_id",
        String,
        ForeignKey("orders.order_id"),
        primary_key=True,
        doc="ID заказа.",
    ),
    Column(
        "product_id",
        Integer,
        ForeignKey("products.id"),
        primary_key=True,
        doc="ID товара.",
    ),
    Column(
        "quantity", Integer, nullable=False, doc="Количество товара в заказе."
    ),
)


class OrderModel(Base):
    """
    Модель заказа.

    Представляет таблицу `orders` в базе данных.
    Содержит информацию о заказе, связанном пользователе и списке товаров.
    """

    __tablename__ = "orders"

    order_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: f"ORD-{uuid.uuid4().hex[:8].upper()}",
        doc="Уникальный идентификатор заказа (генерируется автоматически).",
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        doc="ID пользователя, оформившего заказ (внешний ключ на таблицу users).",
    )

    total: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        doc="Общая сумма заказа (в рублях).",
    )

    create_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        default=datetime.datetime.utcnow,
        doc="Дата и время создания заказа (UTC).",
    )

    # связи
    user: Mapped["UserModel"] = relationship(
        back_populates="orders",
        doc="Объект пользователя, оформившего заказ (связь 1→много).",
    )

    products: Mapped[List["ProductModel"]] = relationship(
        secondary=product_in_order,
        back_populates="orders",
        doc="Список товаров, входящих в заказ (связь многие→многим).",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление заказа (для отладки и логов)."""
        return (
            f"<Order("
            f"id={self.order_id}, "
            f"user_id={self.user_id}, "
            f"total={self.total}, "
            f"created_at={self.create_date})>"
        )
