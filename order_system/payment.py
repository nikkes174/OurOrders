from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from random import choice

from sqlalchemy.orm import Session

from order_system.order import Order


class PaymentSelection(ABC):
    """Абстрактный интерфейс платёжного процессора."""

    @abstractmethod
    def generate_payment_link(self, order: "Order") -> str:
        """Создаёт ссылку для оплаты."""
        pass

    @abstractmethod
    def order_status(self, order_id: str, order_obj: "Order") -> bool:
        """Проверяет статус оплаты."""
        pass


class CreditCardPayment(PaymentSelection):
    """Оплата через банковскую карту."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def generate_payment_link(self, order: "Order") -> str:
        """Генерация ссылки на оплату через банковскую карту."""
        base_url = "https://sberbank.example.com/pay"
        transaction_id = uuid.uuid4().hex[:8].upper()
        return (
            f"{base_url}?order_id={order.create_order_id()}&tx={transaction_id}"
            f"&amount={order.total}&method=card"
        )

    def order_status(self, order_id: str, order_obj: "Order") -> bool:
        """Эмуляция успешной оплаты по карте и сохранение заказа."""
        # импортируем внутри метода, чтобы избежать циклов импорта
        from order_system.order import Order

        service = Order(self.session, order_obj.basket, order_obj.user)
        service.create_order_in_db(order_obj)
        return True


class PayPalPayment(PaymentSelection):
    """Оплата через PayPal."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def generate_payment_link(self, order: "Order") -> str:
        """Генерация ссылки для оплаты через PayPal."""
        base_url = "https://www.paypal.com/checkout"
        session_id = uuid.uuid4().hex[:6].upper()
        return (
            f"{base_url}?order={order.create_order_id()}&session={session_id}"
            f"&amount={order.total}"
        )

    def order_status(self, order_id: str, order_obj: "Order") -> bool:
        """Проверка статуса оплаты через PayPal (эмуляция 50/50)."""
        from order_system.order import Order

        status = choice([True, False])
        if status:
            service = Order(self.session, order_obj.basket, order_obj.user)
            service.create_order_in_db(order_obj)
        return status


class CryptoPayment(PaymentSelection):
    """Оплата через криптовалюту."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def generate_payment_link(self, order: "Order") -> str:
        """Генерация ссылки на оплату через криптокошелёк."""
        base_url = "https://crypto-pay.example.com/invoice"
        tx_hash = uuid.uuid4().hex[:10].upper()
        return (
            f"{base_url}?order={order.create_order_id()}&tx_hash={tx_hash}"
            f"&amount={order.total}&currency=USDT"
        )

    def order_status(self, order_id: str, order_obj: "Order") -> bool:
        """Проверка статуса оплаты через криптовалюту."""
        from order_system.order import Order

        status = choice([True, False])
        if status:
            service = Order(self.session, order_obj.basket, order_obj.user)
            service.create_order_in_db(order_obj)
        return status
