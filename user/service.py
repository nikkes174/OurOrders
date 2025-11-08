from __future__ import annotations

from sqlalchemy.orm import Session

from user.models import UserModel


class ActionsWithUser:
    """Класс для работы с пользователями."""

    def __init__(self, session: Session) -> None:
        """Инициализация сервиса работы с пользователями."""
        self.session = session

    def add_user(
        self, name: str, age: int, email: str, phone: str
    ) -> UserModel:
        """
        Добавляет нового пользователя в базу данных.

        :param name: Имя пользователя.
        :param age: Возраст пользователя.
        :param email: Email (уникальный).
        :param phone: Телефон (уникальный).
        :raises ValueError: Если пользователь с таким email уже существует.
        :return: Объект созданного пользователя.
        """
        existing_user = (
            self.session.query(UserModel)
            .filter(UserModel.email == email)
            .first()
        )

        if existing_user:
            raise ValueError(f"Пользователь с email {email} уже существует.")

        new_user = UserModel(name=name, age=age, email=email, phone=phone)
        self.session.add(new_user)
        self.session.commit()
        return new_user
