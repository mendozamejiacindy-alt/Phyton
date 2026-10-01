from abc import ABC, abstractmethod

from .models import Product


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_price(self, product: Product) -> float:
        """Calcula el precio final del producto."""
        raise NotImplementedError


class RegularPriceStrategy(PricingStrategy):
    def calculate_price(self, product: Product) -> float:
        return product.price


class DiscountPriceStrategy(PricingStrategy):
    def __init__(self, discount: float) -> None:
        if not 0 <= discount <= 1:
            raise ValueError("El descuento debe estar entre 0 y 1.")

        self.discount = discount

    def calculate_price(self, product: Product) -> float:
        return product.price * (1 - self.discount)


class PremiumPriceStrategy(PricingStrategy):
    def calculate_price(self, product: Product) -> float:
        return product.price * 0.90
