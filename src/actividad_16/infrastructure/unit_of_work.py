import types
from typing import Self

from actividad_16.application.ports import OrderRepository, UnitOfWork
from actividad_16.infrastructure.memory_repository import MemoryOrderRepository


class MemoryUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.orders: OrderRepository = MemoryOrderRepository()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: types.TracebackType | None,
    ) -> None:
        return None

    def commit(self) -> None:
        return None
