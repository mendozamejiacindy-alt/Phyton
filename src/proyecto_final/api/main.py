from uuid import UUID

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from proyecto_final.infrastructure.event_publisher import ConsoleEventPublisher

from proyecto_final.application.use_cases import (
    CreateOrder,
    DeleteOrder,
    GetOrder,
    ListOrders,
)
from proyecto_final.infrastructure.memory_repository import (
    InMemoryOrderRepository,
)

app = FastAPI(
    title="Orders API",
    description="API del Proyecto Final - Arquitectura Hexagonal/Limpia",
    version="1.0.0",
)

repository = InMemoryOrderRepository()
event_publisher = ConsoleEventPublisher()

create_order = CreateOrder(repository, event_publisher)
get_order = GetOrder(repository)
list_orders = ListOrders(repository)
delete_order = DeleteOrder(repository)


class OrderRequest(BaseModel):
    product: str
    quantity: int
    price: float


@app.get("/orders")
def get_orders():
    return list_orders.execute()


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: UUID):
    order = get_order.execute(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@app.post("/orders")
def create_new_order(request: OrderRequest):
    return create_order.execute(
        product=request.product,
        quantity=request.quantity,
        price=request.price,
    )


@app.delete("/orders/{order_id}")
def delete_order_by_id(order_id: UUID):
    order = get_order.execute(order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    delete_order.execute(order_id)

    return {"message": "Order deleted successfully"}
