import asyncio
import time
from concurrent.futures import ProcessPoolExecutor

import httpx

URLS = [
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
    "https://example.com",
]


def fetch_sincrono(urls: list[str]) -> list[int]:
    resultados = []

    with httpx.Client(timeout=10) as client:
        for url in urls:
            respuesta = client.get(url)
            resultados.append(respuesta.status_code)

    return resultados


async def obtener_url(
    client: httpx.AsyncClient,
    url: str,
    semaforo: asyncio.Semaphore,
) -> int:
    async with semaforo:
        respuesta = await client.get(url)
        return respuesta.status_code


async def fetch_concurrente(
    urls: list[str],
    limite_concurrencia: int = 3,
) -> list[int]:
    semaforo = asyncio.Semaphore(limite_concurrencia)

    async with httpx.AsyncClient(timeout=10) as client:
        tareas = [obtener_url(client, url, semaforo) for url in urls]

        return await asyncio.gather(*tareas)


def calcular_cpu(numero: int) -> int:
    resultado = 0

    for valor in range(numero):
        resultado += valor * valor

    return resultado


def calcular_con_procesos(numeros: list[int]) -> list[int]:
    with ProcessPoolExecutor() as executor:
        return list(executor.map(calcular_cpu, numeros))


def main() -> None:
    inicio = time.perf_counter()

    resultados_sincronos = fetch_sincrono(URLS)

    tiempo_sincrono = time.perf_counter() - inicio

    inicio = time.perf_counter()

    resultados_concurrentes = asyncio.run(fetch_concurrente(URLS))

    tiempo_concurrente = time.perf_counter() - inicio

    print("=== EJECUCIÓN SÍNCRONA ===")
    print("Códigos HTTP:", resultados_sincronos)
    print(f"Tiempo: {tiempo_sincrono:.2f} segundos")

    print()

    print("=== EJECUCIÓN CONCURRENTE ===")
    print("Códigos HTTP:", resultados_concurrentes)
    print(f"Tiempo: {tiempo_concurrente:.2f} segundos")

    print()

    numeros = [100_000, 100_000, 100_000, 100_000]

    inicio = time.perf_counter()

    resultados_cpu = calcular_con_procesos(numeros)

    tiempo_cpu = time.perf_counter() - inicio

    print("=== CPU-BOUND CON PROCESOS ===")
    print("Resultados:", resultados_cpu)
    print(f"Tiempo: {tiempo_cpu:.2f} segundos")


if __name__ == "__main__":
    main()
