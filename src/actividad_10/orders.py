from collections.abc import Callable


def calcular_total(precio: float, cantidad: int) -> float:
    return precio * cantidad


def obtener_precio(
    producto: str,
    consulta_precio: Callable[[str], float],
) -> float:
    return consulta_precio(producto)


def calcular_total_producto(
    producto: str,
    cantidad: int,
    consulta_precio: Callable[[str], float],
) -> float:
    precio = obtener_precio(producto, consulta_precio)

    return precio * cantidad
