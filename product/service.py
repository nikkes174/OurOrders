from __future__ import annotations

from sqlalchemy.orm import Session

from product.models import ProductModel


class ProductService:
    """Сервис для получения данных о товарах."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_stock_product(self, title: str) -> int | None:
        """Возвращает остаток товара по названию."""
        stock = (
            self.session.query(ProductModel.stock)
            .filter(ProductModel.title == title)
            .first()
        )
        return stock[0] if stock else None

    def get_price_product(self, title: str) -> float | None:
        """Возвращает цену товара по названию."""
        price = (
            self.session.query(ProductModel.price)
            .filter(ProductModel.title == title)
            .first()
        )
        return price[0] if price else None

    def get_title_product(self, title: str) -> str | None:
        """Возвращает название товара (если найден)."""
        result = (
            self.session.query(ProductModel.title)
            .filter(ProductModel.title == title)
            .first()
        )
        return result[0] if result else None
