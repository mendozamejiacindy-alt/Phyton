from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    id: int
    product: str
    quantity: int
    price: float

    @property
    def total(self) -> float:
        return self.quantity * self.price
