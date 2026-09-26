from dataclasses import dataclass, field
from functools import total_ordering

from pydantic import BaseModel, Field

# ============================================================
# DATACLASS: Order
# ============================================================


@total_ordering
@dataclass
class Order:
    order_id: int
    customer: str
    items: list[tuple[str, float, int]] = field(default_factory=list)

    @property
    def total(self) -> float:
        """Calcula el total de la orden."""
        return sum(price * quantity for _, price, quantity in self.items)

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        """Agrega un producto a la orden."""
        self.items.append((name, price, quantity))

    def __eq__(self, other: object) -> bool:
        """Compara dos órdenes por su total."""
        if not isinstance(other, Order):
            return NotImplemented

        return self.total == other.total

    def __lt__(self, other: object) -> bool:
        """Permite ordenar órdenes por su total."""
        if not isinstance(other, Order):
            return NotImplemented

        return self.total < other.total


# ============================================================
# MODELOS PYDANTIC
# ============================================================


class OrderIn(BaseModel):
    order_id: int = Field(gt=0)
    customer: str = Field(min_length=1)
    items: list[tuple[str, float, int]]


class OrderOut(BaseModel):
    order_id: int
    customer: str
    total: float


# ============================================================
# CONVERSIÓN DE MODELO PYDANTIC A ENTIDAD
# ============================================================


def convertir_a_entidad(order_in: OrderIn) -> Order:
    """Convierte un OrderIn de Pydantic en una entidad Order."""
    return Order(
        order_id=order_in.order_id,
        customer=order_in.customer,
        items=order_in.items,
    )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================


if __name__ == "__main__":
    print("=== DATACLASS ORDER ===")

    order_1 = Order(
        order_id=1,
        customer="Ana",
        items=[
            ("Laptop", 15000.0, 1),
            ("Mouse", 500.0, 2),
        ],
    )

    order_2 = Order(
        order_id=2,
        customer="María",
        items=[
            ("Teclado", 1200.0, 1),
            ("Monitor", 5000.0, 1),
        ],
    )

    print(f"Orden 1: {order_1.customer}")
    print(f"Total orden 1: ${order_1.total:.2f}")

    print(f"Orden 2: {order_2.customer}")
    print(f"Total orden 2: ${order_2.total:.2f}")

    print(f"¿Orden 1 es mayor que Orden 2?: {order_1 > order_2}")

    print("\n=== PYDANTIC ORDERIN ===")

    datos = {
        "order_id": 3,
        "customer": "Carlos",
        "items": [
            ("Celular", 8000.0, 1),
            ("Funda", 300.0, 2),
        ],
    }

    order_in = OrderIn(**datos)

    print(f"OrderIn: {order_in}")

    print("\n=== CONVERSIÓN A ENTIDAD ===")

    order = convertir_a_entidad(order_in)

    print(f"Cliente: {order.customer}")
    print(f"Total: ${order.total:.2f}")

    print("\n=== ORDEROUT ===")

    order_out = OrderOut(
        order_id=order.order_id,
        customer=order.customer,
        total=order.total,
    )

    print(order_out)
