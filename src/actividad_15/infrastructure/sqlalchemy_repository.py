from decimal import Decimal
from uuid import UUID

from sqlalchemy import Integer, Numeric, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from actividad_15.domain.entities import Order


class Base(DeclarativeBase):
    """Base para los modelos de SQLAlchemy."""


class OrderModel(Base):
    """Modelo de persistencia de una orden."""

    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    product: Mapped[str] = mapped_column(String(200), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)


class SQLAlchemyOrderRepository:
    """Adaptador de repositorio utilizando SQLAlchemy."""

    def __init__(
        self,
        database_url: str = "sqlite+pysqlite:///:memory:",
    ) -> None:
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)

    def save(self, order: Order) -> Order:
        """Guarda una orden en la base de datos."""
        with Session(self.engine) as session:
            model = OrderModel(
                id=str(order.id),
                product=order.product,
                quantity=order.quantity,
                price=order.price,
            )

            session.add(model)
            session.commit()

        return order

    def get_by_id(self, order_id: UUID) -> Order | None:
        """Busca una orden por su identificador."""
        with Session(self.engine) as session:
            model = session.get(OrderModel, str(order_id))

            if model is None:
                return None

            return Order(
                id=UUID(model.id),
                product=model.product,
                quantity=model.quantity,
                price=Decimal(str(model.price)),
            )
