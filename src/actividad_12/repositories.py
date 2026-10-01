import sqlite3

from .models import Order


class MemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[int, Order] = {}

    def save(self, order: Order) -> None:
        self._orders[order.id] = order

    def get(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)


class SqlOrderRepository:
    def __init__(self, connection: sqlite3.Connection | None = None) -> None:
        self.connection = connection or sqlite3.connect(":memory:")

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
            """)

        self.connection.commit()

    def save(self, order: Order) -> None:
        self.connection.execute(
            """
            INSERT OR REPLACE INTO orders
            (id, product, quantity, price)
            VALUES (?, ?, ?, ?)
            """,
            (
                order.id,
                order.product,
                order.quantity,
                order.price,
            ),
        )

        self.connection.commit()

    def get(self, order_id: int) -> Order | None:
        cursor = self.connection.execute(
            """
            SELECT id, product, quantity, price
            FROM orders
            WHERE id = ?
            """,
            (order_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Order(
            id=row[0],
            product=row[1],
            quantity=row[2],
            price=row[3],
        )
