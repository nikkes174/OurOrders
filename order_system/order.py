from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Union

from sqlalchemy.orm import Session

from order.models import OrderModel, product_in_order
from product.models import ProductModel
from product.service import ProductService

if TYPE_CHECKING:
    from user.models import UserModel


class Basket:
    """Класс, отвечающий за хранение и управление товарами в корзине пользователя."""

    def __init__(self, product_service: ProductService) -> None:
        self.product_service = product_service
        self.list_items: dict[str, dict[str, float | int]] = {}

    def add_item(self, title: str, quantity: int) -> None:
        price = self.product_service.get_price_product(title)
        stock = self.product_service.get_stock_product(title)

        if stock is None or price is None:
            raise ValueError(f"Товар {title} не найден в базе данных!")

        if stock < quantity:
            raise ValueError("Недостаточное количество товара на складе")

        if title in self.list_items:
            quantity = int(quantity + self.list_items[title]["quantity"])

        self.list_items[title] = {
            "quantity": quantity,
            "total": price * quantity,
        }
        print(
            f"Товар {title} в количестве {quantity} шт. добавлен в корзину. "
            f"Общая стоимость: {self.list_items[title]['total']}"
        )

    def delete_item(self, title: str) -> None:
        self.list_items.pop(title, None)

    def change_quantity(self, title: str, subtractible_quantity: int) -> None:
        current_quantity = self.list_items[title].get("quantity", 0)
        if current_quantity < subtractible_quantity:
            raise ValueError("Вы хотите убрать больше, чем есть в корзине")

        new_quantity = current_quantity - subtractible_quantity
        if new_quantity == 0:
            self.delete_item(title)
            return

        price_per_item = self.list_items[title]["total"] / current_quantity
        self.list_items[title]["quantity"] = new_quantity
        self.list_items[title]["total"] = price_per_item * new_quantity

        print(
            f"Количество товара {title} изменено. "
            f"Теперь {new_quantity} шт. (на сумму {self.list_items[title]['total']})"
        )

    def get_total(self) -> float:
        return sum(item["total"] for item in self.list_items.values())

    def get_list_items(self) -> dict[str, dict[str, Union[int, float]]]:
        return self.list_items

    def is_empty(self) -> bool:
        return not bool(self.list_items)


class Order:
    """Класс, отвечающий за формирование заказа на основе корзины пользователя."""

    def __init__(
        self, session: Session, basket: Basket, user: "UserModel"
    ) -> None:
        if basket.is_empty():
            raise ValueError("Нельзя создать заказ из пустой корзины")

        self.session = session
        self.basket = basket
        self.user = user
        self.user_id = user.id
        self.total = basket.get_total()

    def create_order_id(self) -> str:
        random_part = uuid.uuid4().hex[:6].upper()
        return f"ORD-{self.user_id}-{random_part}"

    def create_order(
        self,
    ) -> dict[str, Union[str, int, float, dict[str, dict[str, Any]]]]:
        return {
            "order_id": self.create_order_id(),
            "user_id": self.user_id,
            "items": self.basket.get_list_items(),
            "total": self.basket.get_total(),
        }

    def create_order_in_db(self, order_obj: "Order") -> "OrderModel":

        new_order = OrderModel(
            user_id=order_obj.user_id, total=order_obj.total
        )
        self.session.add(new_order)
        self.session.flush()

        for title, item in order_obj.basket.get_list_items().items():
            product = (
                self.session.query(ProductModel)
                .filter_by(title=title)  # <-- вот это важно
                .first()
            )
            if not product:
                raise ValueError(f"Товар {title} не найден в каталоге!")

            self.session.execute(
                product_in_order.insert().values(
                    order_id=new_order.order_id,
                    product_id=product.id,
                    quantity=item["quantity"],
                )
            )

        self.session.commit()
        return new_order
