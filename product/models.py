from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from order.models import product_in_order
from order_system.db import Base

if TYPE_CHECKING:
    from order.models import OrderModel


class ProductModel(Base):
    """Модель товара.

    Представляет таблицу `products` в базе данных.
    """

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        doc="Уникальный идентификатор товара.",
    )

    title: Mapped[str] = mapped_column(
        String(256), nullable=False, doc="Название товара."
    )

    price: Mapped[float] = mapped_column(
        Float, nullable=False, doc="Цена товара (в рублях)."
    )

    stock: Mapped[int] = mapped_column(
        Integer, nullable=False, doc="Доступное кол-во товара на складе."
    )

    # связь с заказами
    orders: Mapped[List["OrderModel"]] = relationship(
        secondary=product_in_order,
        back_populates="products",
        doc="Список заказов, в которых участвует этот товар.",
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление товара (для логов и отладки)."""
        return (
            f"<Товар("
            f"id={self.id}, "
            f"название='{self.title}', "
            f"остаток={self.stock}, "
            f"цена={self.price})>"
        )
