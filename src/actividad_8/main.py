from .crud import (
    agregar_producto,
    crear_orden,
    crear_usuario,
    obtener_ordenes,
    obtener_usuarios,
)
from .database import crear_base_de_datos, obtener_sesion


def main() -> None:
    """Ejecuta una demostración del CRUD con SQLAlchemy."""
    print("=== ACTIVIDAD 8: SQLALCHEMY ORM ===")

    crear_base_de_datos()

    with obtener_sesion() as session:
        print("\n=== CREAR USUARIO ===")

        usuario = crear_usuario(
            session,
            "Ana López",
            "ana@example.com",
        )

        print(f"Usuario creado: {usuario.name}")
        print(f"Email: {usuario.email}")

        print("\n=== CREAR ORDEN ===")

        orden = crear_orden(
            session,
            usuario,
        )

        print(f"Orden creada: {orden.id}")

        print("\n=== AGREGAR PRODUCTOS ===")

        agregar_producto(
            session,
            orden,
            "Laptop",
            1,
            15000.0,
        )

        agregar_producto(
            session,
            orden,
            "Mouse",
            2,
            500.0,
        )

        print(f"Total de la orden: ${orden.total:.2f}")

        print("\n=== CONSULTAR USUARIOS ===")

        usuarios = obtener_usuarios(session)

        for usuario_actual in usuarios:
            print(
                f"ID: {usuario_actual.id} | "
                f"Nombre: {usuario_actual.name} | "
                f"Email: {usuario_actual.email}"
            )

        print("\n=== CONSULTAR ÓRDENES ===")

        ordenes = obtener_ordenes(
            session,
            usuario.id,
        )

        for orden_actual in ordenes:
            print(f"Orden: {orden_actual.id} | " f"Total: ${orden_actual.total:.2f}")

            for item in orden_actual.items:
                print(
                    f"  Producto: {item.product} | "
                    f"Cantidad: {item.quantity} | "
                    f"Precio: ${item.price:.2f}"
                )


if __name__ == "__main__":
    main()
