from collections.abc import Callable


class PriceCacheDecorator:
    def __init__(self, price_function: Callable[[str], float]) -> None:
        self.price_function = price_function
        self.cache: dict[str, float] = {}

    def get_price(self, product_name: str) -> float:
        if product_name not in self.cache:
            self.cache[product_name] = self.price_function(product_name)

        return self.cache[product_name]
