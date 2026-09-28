import time
from functools import wraps
from time import perf_counter


# Decorador de reintentos con backoff
def retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for intento in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as error:
                    if intento == max_retries - 1:
                        raise

                    espera = delay * (2**intento)
                    print(f"Intento {intento + 1} fallido: {error}")
                    print(f"Esperando {espera} segundos...")
                    time.sleep(espera)

        return wrapper

    return decorator


# Función que utiliza el decorador
@retry(max_retries=3, delay=1)
def operacion():
    if not hasattr(operacion, "intentos"):
        operacion.intentos = 0

    operacion.intentos += 1

    if operacion.intentos < 3:
        raise RuntimeError("La operación falló.")

    print("Operación realizada correctamente.")


# Generador por lotes
def generar_lotes(datos, tamaño):
    for inicio in range(0, len(datos), tamaño):
        yield datos[inicio : inicio + tamaño]


# Context manager para medir tiempo
class medir_tiempo:
    def __enter__(self):
        self.inicio = perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        tiempo = perf_counter() - self.inicio
        print(f"Procesamiento: {tiempo:.4f} segundos")


# Programa principal
if __name__ == "__main__":
    print("=== Decorador de reintentos ===")
    operacion()

    print("\n=== Generador por lotes ===")
    datos = list(range(1, 11))

    for lote in generar_lotes(datos, 3):
        print(f"Lote: {lote}")

    print("\n=== Context manager de temporización ===")

    with medir_tiempo():
        time.sleep(1)
