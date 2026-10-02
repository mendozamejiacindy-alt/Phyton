from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Order:
    product: str
    quantity: int
    price: Decimal
    id: UUID | None = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid4()

    def total(self) -> Decimal:
        return self.price * self.quantity
