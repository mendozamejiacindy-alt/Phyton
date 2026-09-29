from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Order, OrderItem, User


def crear_usuario(
    session: Session,
    nombre: str,
    email: str,
) -> User:
    """Crea un usuario."""
    usuario = User(
        name=nombre,
        email=email,
    )

    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    return usuario


def crear_orden(
    session: Session,
    usuario: User,
) -> Order:
    """Crea una orden para un usuario."""
    orden = Order(
        user_id=usuario.id,
        total=0.0,
    )

    session.add(orden)
    session.commit()
    session.refresh(orden)

    return orden


def agregar_producto(
    session: Session,
    orden: Order,
    producto: str,
    cantidad: int,
    precio: float,
) -> OrderItem:
    """Agrega un producto a una orden."""
    item = OrderItem(
        order_id=orden.id,
        product=producto,
        quantity=cantidad,
        price=precio,
    )

    session.add(item)

    orden.total += cantidad * precio

    session.commit()
    session.refresh(item)
    session.refresh(orden)

    return item


def obtener_usuarios(session: Session) -> list[User]:
    """Obtiene todos los usuarios."""
    consulta = select(User).order_by(User.id)

    return list(session.scalars(consulta).all())


def obtener_ordenes(
    session: Session,
    usuario_id: int,
) -> list[Order]:
    """Obtiene las órdenes de un usuario."""
    consulta = select(Order).where(Order.user_id == usuario_id).order_by(Order.id)

    return list(session.scalars(consulta).all())


def eliminar_usuario(
    session: Session,
    usuario_id: int,
) -> bool:
    """Elimina un usuario por su ID."""
    usuario = session.get(User, usuario_id)

    if usuario is None:
        return False

    session.delete(usuario)
    session.commit()

    return True
