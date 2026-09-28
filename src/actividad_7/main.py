import logging
from pathlib import Path
from time import sleep

import httpx

# ============================================================
# CONFIGURACIÓN
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_SALIDA = BASE_DIR / "respuesta_api.json"


# ============================================================
# CONFIGURACIÓN HTTP
# ============================================================

TIMEOUT = httpx.Timeout(
    connect=5.0,
    read=10.0,
    write=10.0,
    pool=5.0,
)

MAX_REINTENTOS = 3


# ============================================================
# CLIENTE HTTP
# ============================================================


def crear_cliente() -> httpx.Client:
    """Crea un cliente HTTP con configuración de timeout."""
    return httpx.Client(
        timeout=TIMEOUT,
        follow_redirects=True,
    )


# ============================================================
# PETICIÓN CON REINTENTOS
# ============================================================


def obtener_datos(
    cliente: httpx.Client,
    url: str,
) -> httpx.Response:
    """Realiza una petición GET con reintentos."""

    ultimo_error: Exception | None = None

    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            logger.info(
                "Realizando petición. Intento %d de %d",
                intento,
                MAX_REINTENTOS,
            )

            respuesta = cliente.get(url)

            respuesta.raise_for_status()

            logger.info(
                "Petición exitosa. Código HTTP: %d",
                respuesta.status_code,
            )

            return respuesta

        except (
            httpx.TimeoutException,
            httpx.NetworkError,
            httpx.HTTPStatusError,
        ) as error:
            ultimo_error = error

            logger.warning(
                "Error en el intento %d: %s",
                intento,
                error,
            )

            if intento < MAX_REINTENTOS:
                sleep(1)

    raise RuntimeError(
        "No fue posible obtener la respuesta después " f"de {MAX_REINTENTOS} intentos."
    ) from ultimo_error


# ============================================================
# STREAMING
# ============================================================


def descargar_streaming(
    cliente: httpx.Client,
    url: str,
    destino: Path,
) -> None:
    """Descarga una respuesta mediante streaming."""

    logger.info("Iniciando descarga por streaming: %s", url)

    try:
        with cliente.stream("GET", url) as respuesta:
            respuesta.raise_for_status()

            with destino.open("wb") as archivo:
                for bloque in respuesta.iter_bytes(chunk_size=8192):
                    archivo.write(bloque)

        logger.info(
            "Descarga completada: %s",
            destino,
        )

    except httpx.HTTPError as error:
        logger.error(
            "Error durante la descarga: %s",
            error,
        )
        raise


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================


def main() -> None:
    """Ejecuta la actividad de consumo de APIs."""

    url_api = "https://jsonplaceholder.typicode.com/todos/1"

    logger.info("Iniciando Actividad 7")

    with crear_cliente() as cliente:
        try:
            respuesta = obtener_datos(
                cliente,
                url_api,
            )

            datos = respuesta.json()

            print("\n=== RESPUESTA DE LA API ===")
            print(f"ID: {datos['id']}")
            print(f"Título: {datos['title']}")
            print(f"Completado: {datos['completed']}")

            ARCHIVO_SALIDA.write_text(
                respuesta.text,
                encoding="utf-8",
            )

            logger.info(
                "Respuesta guardada en: %s",
                ARCHIVO_SALIDA,
            )

            url_streaming = "https://jsonplaceholder.typicode.com/" "todos/1"

            archivo_streaming = BASE_DIR / "descarga_streaming.json"

            descargar_streaming(
                cliente,
                url_streaming,
                archivo_streaming,
            )

        except (
            httpx.HTTPError,
            RuntimeError,
            OSError,
        ) as error:
            logger.error(
                "La actividad terminó con error: %s",
                error,
            )
            raise

    logger.info("Actividad 7 finalizada correctamente")


if __name__ == "__main__":
    main()
