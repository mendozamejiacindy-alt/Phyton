from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price: float


@dataclass(frozen=True)
class ExternalProduct:
    product_name: str
    amount: float
