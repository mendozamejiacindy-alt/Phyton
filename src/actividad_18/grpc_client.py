import grpc

from actividad_18.proto import orders_pb2, orders_pb2_grpc


def main() -> None:
    with grpc.insecure_channel("localhost:50051") as channel:
        client = orders_pb2_grpc.OrderServiceStub(channel)

        print("Conectando al servidor gRPC...")

        # Crear una orden
        create_request = orders_pb2.CreateOrderRequest(
            product="Laptop",
            quantity=2,
            price=15000.00,
        )

        created_order = client.CreateOrder(create_request)

        print("\nOrden creada:")
        print(f"ID: {created_order.order_id}")
        print(f"Producto: {created_order.product}")
        print(f"Cantidad: {created_order.quantity}")
        print(f"Precio: ${created_order.price:.2f}")
        print(f"Estado: {created_order.status}")

        # Consultar la orden creada
        get_request = orders_pb2.GetOrderRequest(
            order_id=created_order.order_id,
        )

        order = client.GetOrder(get_request)

        print("\nOrden consultada:")
        print(f"ID: {order.order_id}")
        print(f"Producto: {order.product}")
        print(f"Cantidad: {order.quantity}")
        print(f"Precio: ${order.price:.2f}")
        print(f"Estado: {order.status}")


if __name__ == "__main__":
    main()
