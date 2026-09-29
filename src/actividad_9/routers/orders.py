from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import obtener_sesion
from ..dependencies import obtener_usuario_actual
from ..models import Order
from ..schemas import OrderCreate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(obtener_usuario_actual)],
)
def crear_order(
    order: OrderCreate,
    db: Session = Depends(obtener_sesion),
) -> Order:
    nueva_order = Order(
        product=order.product,
        quantity=order.quantity,
        price=order.price,
    )

    db.add(nueva_order)
    db.commit()
    db.refresh(nueva_order)

    return nueva_order


@router.get(
    "/",
    response_model=list[OrderResponse],
    dependencies=[Depends(obtener_usuario_actual)],
)
def obtener_orders(
    db: Session = Depends(obtener_sesion),
) -> list[Order]:
    return db.query(Order).all()


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    dependencies=[Depends(obtener_usuario_actual)],
)
def obtener_order(
    order_id: int,
    db: Session = Depends(obtener_sesion),
) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order no encontrada",
        )

    return order


@router.put(
    "/{order_id}",
    response_model=OrderResponse,
    dependencies=[Depends(obtener_usuario_actual)],
)
def actualizar_order(
    order_id: int,
    order_data: OrderCreate,
    db: Session = Depends(obtener_sesion),
) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order no encontrada",
        )

    order.product = order_data.product
    order.quantity = order_data.quantity
    order.price = order_data.price

    db.commit()
    db.refresh(order)

    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(obtener_usuario_actual)],
)
def eliminar_order(
    order_id: int,
    db: Session = Depends(obtener_sesion),
) -> None:
    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order no encontrada",
        )

    db.delete(order)
    db.commit()
