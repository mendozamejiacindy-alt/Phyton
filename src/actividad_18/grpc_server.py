from concurrent import futures
from uuid import uuid4

import grpc

from actividad_18.proto import orders_pb2, orders_pb2_grpc
from actividad_18.redis_events import publish_order_created


class OrderService(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self) -> None:
        self.orders: dict[str, orders_pb2.OrderResponse] = {}

    def CreateOrder(
        self,
        request: orders_pb2.CreateOrderRequest,
        context: grpc.ServicerContext,
    ) -> orders_pb2.OrderResponse:
        order_id = str(uuid4())

        order = orders_pb2.OrderResponse(
            order_id=order_id,
            product=request.product,
            quantity=request.quantity,
            price=request.price,
            status="CREATED",
        )

        self.orders[order_id] = order

        publish_order_created(
            order_id=order.order_id,
            product=order.product,
            quantity=order.quantity,
            price=order.price,
        )

        return order

    def GetOrder(
        self,
        request: orders_pb2.GetOrderRequest,
        context: grpc.ServicerContext,
    ) -> orders_pb2.OrderResponse:
        order = self.orders.get(request.order_id)

        if order is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Order not found",
            )

        return order


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    orders_service = OrderService()

    orders_pb2_grpc.add_OrderServiceServicer_to_server(
        orders_service,
        server,
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("Servidor gRPC ejecutándose en el puerto 50051")

    server.wait_for_termination()


if __name__ == "__main__":
    serve()
