from __future__ import annotations

from typing import TYPE_CHECKING, List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from order_system.db import Base

if TYPE_CHECKING:
    from order.models import OrderModel


class UserModel(Base):
    """Модель пользователя.

    Описывает таблицу `users` в базе данных.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, doc="ID пользователя."
    )
    name: Mapped[str] = mapped_column(
        String(50), nullable=False, doc="Имя пользователя."
    )
    age: Mapped[int] = mapped_column(
        Integer, nullable=False, doc="Возраст пользователя."
    )
    email: Mapped[str] = mapped_column(
        String(120),
        unique=True,
        nullable=False,
        doc="Электронная почта (уникальна).",
    )
    phone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        doc="Номер телефона (уникален).",
    )

    orders: Mapped[List["OrderModel"]] = relationship(
        back_populates="user", doc="Список заказов пользователя."
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление пользователя (для отладки и логов)."""
        return (
            f"Пользователь("
            f"id={self.id}, "
            f"Имя='{self.name}', "
            f"Возраст={self.age}, "
            f"Телефон={self.phone})"
        )
