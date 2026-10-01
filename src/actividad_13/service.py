from .adapters import ProductProviderAdapter
from .models import Product
from .strategies import PricingStrategy


class PricingService:
    def __init__(
        self,
        provider: ProductProviderAdapter,
        strategy: PricingStrategy,
    ) -> None:
        self.provider = provider
        self.strategy = strategy

    def get_final_price(self, product_name: str) -> float:
        product: Product = self.provider.get_product(product_name)

        return self.strategy.calculate_price(product)
