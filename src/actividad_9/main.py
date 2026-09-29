from fastapi import FastAPI

from .auth import router as auth_router
from .database import crear_base_de_datos
from .routers.orders import router as orders_router

app = FastAPI(
    title="Actividad 9 - Orders API",
    description="API REST para gestionar órdenes",
    version="1.0.0",
)


@app.on_event("startup")
def iniciar_aplicacion() -> None:
    crear_base_de_datos()


app.include_router(orders_router)
app.include_router(auth_router)


@app.get("/")
def inicio() -> dict[str, str]:
    return {"mensaje": "API de Orders funcionando"}
