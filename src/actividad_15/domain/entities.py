from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass
class Order:
    """Entidad de dominio que representa una orden."""

    product: str
    quantity: int
    price: Decimal
    id: UUID = field(default_factory=uuid4)

    def total(self) -> Decimal:
        """Calcula el total de la orden."""
        return self.price * self.quantity

    def validate(self) -> None:
        """Valida las reglas básicas de negocio."""
        if not self.product.strip():
            raise ValueError("El producto es obligatorio.")

        if self.quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if self.price <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
