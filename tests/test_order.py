from unittest.mock import MagicMock

import pytest

from order_system.order import Basket, Order


def test_create_order_in_db(mock_session, mock_user, mock_product_service):
    """Проверяем успешное создание заказа (эмуляция без реальной БД)."""

    basket = Basket(mock_product_service)
    basket.add_item("Монитор", 1)

    mock_product = MagicMock(id=1)
    mock_session.query.return_value.filter.return_value.first.return_value = (
        mock_product
    )

    order = Order(mock_session, basket, mock_user)

    result = order.create_order_in_db(order)

    # Проверяем поведение
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    assert result is not None
    assert result.user_id == mock_user.id
    assert result.total == pytest.approx(100.0)


def test_create_order_in_db_product_not_found(
    mock_session, mock_user, mock_product_service
):
    """Проверяем, что выбрасывается ValueError, если товар не найден в каталоге."""

    basket = Basket(mock_product_service)
    basket.add_item("Монитор", 1)

    mock_query = MagicMock()
    mock_filter = MagicMock()

    mock_filter.first.return_value = None
    mock_query.filter_by.return_value = mock_filter
    mock_session.query.return_value = mock_query

    order = Order(mock_session, basket, mock_user)

    with pytest.raises(ValueError, match="не найден в каталоге"):
        order.create_order_in_db(order)
