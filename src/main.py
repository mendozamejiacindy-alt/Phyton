from typing import Literal, Protocol, TypedDict


# Tipado básico
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"


# Literal
def obtener_estado() -> Literal["activo", "inactivo"]:
    return "activo"


# TypedDict
class Usuario(TypedDict):
    nombre: str
    edad: int
    activo: bool


def mostrar_usuario(usuario: Usuario) -> None:
    print(f"Nombre: {usuario['nombre']}")
    print(f"Edad: {usuario['edad']}")
    print(f"Activo: {usuario['activo']}")


# Protocol
class Identificable(Protocol):
    def obtener_id(self) -> int: ...


class Producto:
    def __init__(self, producto_id: int, nombre: str) -> None:
        self.producto_id = producto_id
        self.nombre = nombre

    def obtener_id(self) -> int:
        return self.producto_id


def mostrar_id(objeto: Identificable) -> None:
    print(f"ID: {objeto.obtener_id()}")


# Programa principal
if __name__ == "__main__":
    print("=== TIPADO ESTÁTICO ===")

    mensaje = saludar("Ximena")
    print(mensaje)

    print("\n=== LITERAL ===")
    estado = obtener_estado()
    print(f"Estado: {estado}")

    print("\n=== TYPEDDICT ===")
    usuario: Usuario = {
        "nombre": "Ximena",
        "edad": 22,
        "activo": True,
    }

    mostrar_usuario(usuario)

    print("\n=== PROTOCOL ===")
    producto = Producto(101, "Laptop")
    mostrar_id(producto)
