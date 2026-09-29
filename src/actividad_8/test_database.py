from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .crud import (
    agregar_producto,
    crear_orden,
    crear_usuario,
    obtener_ordenes,
    obtener_usuarios,
)
from .models import Base


def test_crud_en_sqlite_memoria() -> None:
    """Prueba el CRUD usando SQLite en memoria."""

    engine = create_engine(
        "sqlite:///:memory:",
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        usuario = crear_usuario(
            session,
            "Carlos Pérez",
            "carlos@example.com",
        )

        assert usuario.id is not None

        orden = crear_orden(
            session,
            usuario,
        )

        agregar_producto(
            session,
            orden,
            "Teclado",
            2,
            750.0,
        )

        assert orden.total == 1500.0

        usuarios = obtener_usuarios(session)

        assert len(usuarios) == 1
        assert usuarios[0].name == "Carlos Pérez"

        ordenes = obtener_ordenes(
            session,
            usuario.id,
        )

        assert len(ordenes) == 1
        assert ordenes[0].total == 1500.0
