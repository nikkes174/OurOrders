from unittest.mock import MagicMock

import pytest

from product.service import ProductService
from user.service import ActionsWithUser


@pytest.fixture
def mock_session():
    """Фейковая сессия SQLAlchemy."""
    return MagicMock()


@pytest.fixture
def service(mock_session):
    return ProductService(mock_session)


def test_get_stock_product_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        5,
    )
    service = ProductService(mock_session)
    result = service.get_stock_product("Чайник")
    assert result == 5


def test_get_stock_product_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        None
    )
    service = ProductService(mock_session)
    assert service.get_stock_product("Неизвестный") is None


def test_get_price_product_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        1999.99,
    )
    service = ProductService(mock_session)
    assert service.get_price_product("Чайник") == 1999.99


def test_get_price_product_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        None
    )
    service = ProductService(mock_session)
    assert service.get_price_product("Неизвестный") is None


def test_get_title_product_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        "Чайник",
    )
    service = ProductService(mock_session)
    assert service.get_title_product("Чайник") == "Чайник"


def test_get_title_product_not_found(mock_session):
    mock_session.query.return_value.filter.return_value.first.return_value = (
        None
    )
    service = ProductService(mock_session)
    assert service.get_title_product("Неизвестный") is None


@pytest.fixture
def user_service(mock_session):
    return ActionsWithUser(mock_session)


def test_add_user_success(mock_session):
    """Добавление нового пользователя проходит успешно."""
    mock_session.query.return_value.filter.return_value.first.return_value = (
        None
    )
    user_service = ActionsWithUser(mock_session)

    result = user_service.add_user(
        "Иван", 30, "ivan@example.com", "+79991112233"
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result is not None


def test_add_user_already_exists(mock_session):
    """Ошибка при добавлении существующего пользователя."""
    mock_session.query.return_value.filter.return_value.first.return_value = (
        MagicMock()
    )
    user_service = ActionsWithUser(mock_session)

    with pytest.raises(ValueError, match="уже существует"):
        user_service.add_user("Иван", 30, "ivan@example.com", "+79991112233")
