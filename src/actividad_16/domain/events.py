from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class OrderCreated:
    order_id: UUID
    product: str
    quantity: int
