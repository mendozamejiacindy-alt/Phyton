import asyncio

from . import main as main_module
from .main import (
    URLS,
    calcular_con_procesos,
    calcular_cpu,
    fetch_concurrente,
    fetch_sincrono,
)


def test_calcular_cpu():
    resultado = calcular_cpu(10)

    assert resultado == 285


def test_calcular_con_procesos():
    numeros = [10, 20]

    resultados = calcular_con_procesos(numeros)

    assert resultados == [285, 2470]


def test_fetch_sincrono():
    resultados = fetch_sincrono(URLS)

    assert len(resultados) == 5
    assert all(codigo == 200 for codigo in resultados)


def test_fetch_concurrente():
    resultados = asyncio.run(fetch_concurrente(URLS))

    assert len(resultados) == 5
    assert all(codigo == 200 for codigo in resultados)


def test_main(monkeypatch, capsys):
    monkeypatch.setattr(
        main_module,
        "fetch_sincrono",
        lambda urls: [200, 200, 200, 200, 200],
    )

    def fake_asyncio_run(coroutine):
        coroutine.close()
        return [200, 200, 200, 200, 200]

    monkeypatch.setattr(
        main_module.asyncio,
        "run",
        fake_asyncio_run,
    )

    monkeypatch.setattr(
        main_module,
        "calcular_con_procesos",
        lambda numeros: [285, 285, 285, 285],
    )

    main_module.main()

    salida = capsys.readouterr().out

    assert "EJECUCIÓN SÍNCRONA" in salida
    assert "EJECUCIÓN CONCURRENTE" in salida
    assert "CPU-BOUND CON PROCESOS" in salida
