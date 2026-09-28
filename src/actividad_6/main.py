import csv
import json
import logging
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

# ============================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# ============================================================
# MODELO DE DATOS
# ============================================================


@dataclass
class Venta:
    fecha: datetime
    producto: str
    cantidad: int
    precio: float

    @property
    def total(self) -> float:
        """Calcula el total de la venta."""
        return self.cantidad * self.precio


# ============================================================
# LECTURA DEL CSV
# ============================================================


def leer_ventas(ruta: Path) -> list[Venta]:
    """Lee las ventas desde un archivo CSV."""
    ventas: list[Venta] = []

    logger.info("Iniciando lectura del archivo: %s", ruta)

    if not ruta.exists():
        logger.error("El archivo no existe: %s", ruta)
        raise FileNotFoundError(f"No existe el archivo: {ruta}")

    with ruta.open("r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            try:
                fecha_texto = fila["fecha"]

                venta = Venta(
                    fecha=datetime.strptime(
                        fecha_texto,
                        "%Y-%m-%d",
                    ).replace(tzinfo=UTC),
                    producto=fila["producto"],
                    cantidad=int(fila["cantidad"]),
                    precio=float(fila["precio"]),
                )

                ventas.append(venta)

            except (KeyError, ValueError) as error:
                logger.warning(
                    "No se pudo procesar una fila: %s",
                    error,
                )

    logger.info("Se cargaron %d ventas", len(ventas))

    return ventas


# ============================================================
# CÁLCULO DE MÉTRICAS
# ============================================================


def calcular_metricas(ventas: list[Venta]) -> dict[str, object]:
    """Calcula métricas generales de las ventas."""
    logger.info("Calculando métricas")

    if not ventas:
        logger.warning("No existen ventas para calcular métricas")

        return {
            "cantidad_ventas": 0,
            "unidades_vendidas": 0,
            "ingresos_totales": 0.0,
            "promedio_venta": 0.0,
        }

    cantidad_ventas = len(ventas)

    unidades_vendidas = sum(venta.cantidad for venta in ventas)

    ingresos_totales = sum(venta.total for venta in ventas)

    promedio_venta = ingresos_totales / cantidad_ventas

    metricas: dict[str, object] = {
        "cantidad_ventas": cantidad_ventas,
        "unidades_vendidas": unidades_vendidas,
        "ingresos_totales": round(ingresos_totales, 2),
        "promedio_venta": round(promedio_venta, 2),
    }

    logger.info("Métricas calculadas correctamente")

    return metricas


# ============================================================
# EXPORTACIÓN A JSON
# ============================================================


def exportar_json(
    datos: dict[str, object],
    ruta: Path,
) -> None:
    """Exporta las métricas a un archivo JSON."""
    logger.info("Exportando resultados a: %s", ruta)

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False,
        )

    logger.info("Archivo JSON generado correctamente")


# ============================================================
# MOSTRAR VENTAS
# ============================================================


def mostrar_ventas(ventas: list[Venta]) -> None:
    """Muestra las ventas en consola."""
    print("\n=== VENTAS ===")

    for venta in ventas:
        print(
            f"Fecha: {venta.fecha.date()} | "
            f"Producto: {venta.producto} | "
            f"Cantidad: {venta.cantidad} | "
            f"Precio: ${venta.precio:.2f} | "
            f"Total: ${venta.total:.2f}"
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================


def main() -> None:
    """Ejecuta el proceso completo de la actividad."""
    logger.info("Iniciando Actividad 6")

    carpeta = Path(__file__).parent

    archivo_csv = carpeta / "ventas.csv"
    archivo_json = carpeta / "metricas.json"

    ventas = leer_ventas(archivo_csv)

    mostrar_ventas(ventas)

    metricas = calcular_metricas(ventas)

    print("\n=== MÉTRICAS ===")

    for nombre, valor in metricas.items():
        print(f"{nombre}: {valor}")

    exportar_json(metricas, archivo_json)

    print(f"\nJSON generado en: {archivo_json}")

    logger.info("Actividad 6 finalizada correctamente")


if __name__ == "__main__":
    main()
