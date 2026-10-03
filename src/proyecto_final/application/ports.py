from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from proyecto_final.domain.entities import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> Order: ...

    def get_by_id(self, order_id: UUID) -> Order | None: ...

    def list_all(self) -> list[Order]: ...

    def delete(self, order_id: UUID) -> None: ...


class EventPublisher(ABC):
    @abstractmethod
    def publish_order_created(self, order: Order) -> None:
        """Publica el evento de creación de una orden."""
        raise NotImplementedError
