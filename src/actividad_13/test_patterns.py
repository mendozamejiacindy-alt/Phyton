from .adapters import ExternalProvider, ProductProviderAdapter
from .decorators import PriceCacheDecorator
from .models import Product
from .service import PricingService
from .strategies import (
    DiscountPriceStrategy,
    PremiumPriceStrategy,
    RegularPriceStrategy,
)


def test_regular_price_strategy() -> None:
    product = Product(
        name="Laptop",
        price=15000,
    )

    strategy = RegularPriceStrategy()

    assert strategy.calculate_price(product) == 15000


def test_discount_price_strategy() -> None:
    product = Product(
        name="Laptop",
        price=15000,
    )

    strategy = DiscountPriceStrategy(0.20)

    assert strategy.calculate_price(product) == 12000


def test_premium_price_strategy() -> None:
    product = Product(
        name="Laptop",
        price=15000,
    )

    strategy = PremiumPriceStrategy()

    assert strategy.calculate_price(product) == 13500


def test_adapter() -> None:
    external_provider = ExternalProvider()
    adapter = ProductProviderAdapter(external_provider)

    product = adapter.get_product("Laptop")

    assert product.name == "Laptop"
    assert product.price == 15000


def test_price_service() -> None:
    external_provider = ExternalProvider()
    adapter = ProductProviderAdapter(external_provider)

    service = PricingService(
        adapter,
        DiscountPriceStrategy(0.20),
    )

    assert service.get_final_price("Laptop") == 12000


def test_cache_decorator() -> None:
    calls = 0

    def get_price(product_name: str) -> float:
        nonlocal calls
        calls += 1

        prices = {
            "Laptop": 15000,
            "Mouse": 500,
        }

        return prices[product_name]

    cache = PriceCacheDecorator(get_price)

    first_price = cache.get_price("Laptop")
    second_price = cache.get_price("Laptop")

    assert first_price == 15000
    assert second_price == 15000
    assert calls == 1
