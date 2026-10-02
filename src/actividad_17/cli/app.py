import typer

app = typer.Typer(help="CLI para gestionar Orders.")


@app.command()
def list_orders() -> None:
    """Lista las órdenes."""
    typer.echo("Listado de órdenes")


@app.command()
def create(
    product: str,
    quantity: int,
    price: float,
) -> None:
    """Crea una nueva orden."""
    typer.echo(
        f"Orden creada: {product} | " f"Cantidad: {quantity} | " f"Precio: {price}"
    )


@app.command()
def delete(order_id: str) -> None:
    """Elimina una orden."""
    typer.echo(f"Orden eliminada: {order_id}")


if __name__ == "__main__":
    app()
