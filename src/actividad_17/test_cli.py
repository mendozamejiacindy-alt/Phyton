from typer.testing import CliRunner

from actividad_17.cli.app import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "CLI para gestionar Orders" in result.stdout


def test_list_orders() -> None:
    result = runner.invoke(app, ["list-orders"])

    assert result.exit_code == 0
    assert "Listado de órdenes" in result.stdout


def test_create_order() -> None:
    result = runner.invoke(
        app,
        [
            "create",
            "Laptop",
            "2",
            "15000",
        ],
    )

    assert result.exit_code == 0
    assert "Orden creada" in result.stdout
    assert "Laptop" in result.stdout
    assert "Cantidad: 2" in result.stdout


def test_delete_order() -> None:
    result = runner.invoke(
        app,
        [
            "delete",
            "123",
        ],
    )

    assert result.exit_code == 0
    assert "Orden eliminada: 123" in result.stdout
