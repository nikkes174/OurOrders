from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_session():
    """Мок SQLAlchemy сессии."""
    return MagicMock()


@pytest.fixture
def mock_product_service():
    """Мок сервиса продуктов."""
    mock = MagicMock()
    mock.get_price_product.return_value = 100.0
    mock.get_stock_product.return_value = 10
    return mock


@pytest.fixture
def mock_user():
    """Мок пользователя."""
    user = MagicMock()
    user.id = 1
    user.name = "TestUser"
    return user
