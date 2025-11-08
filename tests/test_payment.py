import re
from unittest.mock import MagicMock, patch

from order_system.order import Basket, Order
from order_system.payment import (
    CreditCardPayment,
    CryptoPayment,
    PayPalPayment,
)


def make_filled_order(mock_session):
    """Создаёт фейковый заказ с корзиной и пользователем (без настоящей БД)."""
    mock_product_service = MagicMock()
    mock_product_service.get_price_product.return_value = 100.0
    mock_product_service.get_stock_product.return_value = 10

    basket = Basket(mock_product_service)
    basket.add_item("Чайник", 1)

    mock_user = MagicMock()
    mock_user.id = 1

    mock_product = MagicMock(id=1)
    mock_session.query.return_value.filter.return_value.first.return_value = (
        mock_product
    )

    order = Order(mock_session, basket, mock_user)
    return order


def test_credit_card_generate_payment_link(mock_session):
    order = make_filled_order(mock_session)
    payment = CreditCardPayment(mock_session)
    link = payment.generate_payment_link(order)

    assert link.startswith("https://sberbank.example.com/pay?")
    assert "order_id=" in link
    assert "amount=" in link
    assert "method=card" in link
    assert re.search(r"&tx=[A-Z0-9]{8}", link)


def test_credit_card_order_status(mock_session):
    order = make_filled_order(mock_session)
    payment = CreditCardPayment(mock_session)

    result = payment.order_status(order.create_order_id(), order)
    assert result is True


@patch("order_system.payment.choice", return_value=True)
def test_paypal_order_status_success(mock_choice, mock_session):
    order = make_filled_order(mock_session)
    payment = PayPalPayment(mock_session)

    result = payment.order_status(order.create_order_id(), order)
    assert result is True


@patch("order_system.payment.choice", return_value=False)
def test_paypal_order_status_fail(mock_choice, mock_session):
    order = make_filled_order(mock_session)
    payment = PayPalPayment(mock_session)

    result = payment.order_status(order.create_order_id(), order)
    assert result is False


@patch("order_system.payment.choice", return_value=True)
def test_crypto_order_status_success(mock_choice, mock_session):
    order = make_filled_order(mock_session)
    payment = CryptoPayment(mock_session)

    result = payment.order_status(order.create_order_id(), order)
    assert result is True


@patch("order_system.payment.choice", return_value=False)
def test_crypto_order_status_fail(mock_choice, mock_session):
    order = make_filled_order(mock_session)
    payment = CryptoPayment(mock_session)

    result = payment.order_status(order.create_order_id(), order)
    assert result is False
