import types
from abc import ABC, abstractmethod
from typing import Protocol
from uuid import UUID

from actividad_16.domain.entities import Order


class OrderRepository(Protocol):
    def add(self, order: Order) -> None: ...

    def get_by_id(self, order_id: UUID) -> Order | None: ...


class UnitOfWork(ABC):
    orders: OrderRepository

    @abstractmethod
    def __enter__(self) -> "UnitOfWork": ...

    @abstractmethod
    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None: ...

    @abstractmethod
    def commit(self) -> None: ...
