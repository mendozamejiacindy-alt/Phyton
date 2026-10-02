from fastapi import FastAPI

app = FastAPI(title="Orders API")


orders: list[dict] = []


@app.get("/orders")
def list_orders() -> list[dict]:
    return orders


@app.post("/orders")
def create_order(product: str, quantity: int, price: float) -> dict:
    order = {
        "id": len(orders) + 1,
        "product": product,
        "quantity": quantity,
        "price": price,
    }

    orders.append(order)

    return order


@app.delete("/orders/{order_id}")
def delete_order(order_id: int) -> dict:
    for order in orders:
        if order["id"] == order_id:
            orders.remove(order)
            return {"message": f"Orden eliminada: {order_id}"}

    return {"message": f"Orden no encontrada: {order_id}"}
