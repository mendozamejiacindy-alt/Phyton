from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Order:
    product: str
    quantity: int
    price: float
    id: UUID = field(default_factory=uuid4)
    status: str = "CREATED"

    @property
    def order_id(self) -> UUID:
        return self.id

    def total(self) -> float:
        return self.quantity * self.price
