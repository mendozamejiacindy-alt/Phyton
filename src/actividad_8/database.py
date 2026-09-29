from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base

DATABASE_URL = "sqlite:///:memory:"


engine = create_engine(
    DATABASE_URL,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
)


def crear_base_de_datos() -> None:
    """Crea las tablas de la base de datos."""
    Base.metadata.create_all(bind=engine)


def obtener_sesion() -> Session:
    """Obtiene una sesión para trabajar con la base de datos."""
    return SessionLocal()
