import json


def cargar_datos(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print("Error: no se encontró el archivo.")
    except json.JSONDecodeError:
        print("Error: el archivo JSON no tiene un formato válido.")

    return []


def filtrar_mayores(datos):
    return [persona for persona in datos if persona["edad"] >= 18]


def main():
    datos = cargar_datos("src/actividad_2/datos.json")
    mayores = filtrar_mayores(datos)

    print("Personas mayores de edad:")

    for persona in mayores:
        print(f"{persona['nombre']} - {persona['edad']} años - {persona['ciudad']}")


if __name__ == "__main__":
    main()
