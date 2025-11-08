import datetime
import re

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from order.models import OrderModel, product_in_order
from order_system.db import Base
from product.models import ProductModel
from user.models import UserModel


@pytest.fixture(scope="module")
def engine():
    """Создаём SQLite in-memory базу."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture()
def session(engine):
    """Создаём новую сессию для каждого теста."""
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_order_model_defaults(session):
    """Проверяем дефолтные поля OrderModel."""
    order = OrderModel(user_id=1, total=999.99)
    session.add(order)
    session.commit()

    assert order.order_id.startswith("ORD-")
    assert re.match(r"ORD-[A-Z0-9]{8}", order.order_id)
    assert isinstance(order.create_date, datetime.datetime)
    assert order.total == 999.99
    assert order.user_id == 1


def test_order_model_repr():
    """__repr__ возвращает строку с ключевыми данными."""
    order = OrderModel(user_id=5, total=500)
    result = repr(order)
    assert "user_id=5" in result
    assert "total=500" in result
    assert "<Order(" in result


def test_product_in_order_table_columns():
    """Проверяем структуру промежуточной таблицы."""
    columns = list(product_in_order.columns.keys())
    assert {"order_id", "product_id", "quantity"}.issubset(columns)


def test_user_model_repr():
    """Проверяем строковое представление пользователя."""
    user = UserModel(id=1, name="Test", age=30, email="t@t.com", phone="12345")
    text = repr(user)
    assert "Пользователь" in text
    assert "Имя='Test'" in text
    assert "Возраст=30" in text


def test_product_model_repr():
    """Проверяем __repr__ продукта."""
    product = ProductModel(id=1, title="Чайник", price=1500, stock=10)
    text = repr(product)
    assert "Товар" in text
    assert "Чайник" in text
    assert "1500" in text
    assert "10" in text
