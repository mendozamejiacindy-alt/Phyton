from unittest.mock import Mock

import pytest
from hypothesis import given
from hypothesis import strategies as st

from .orders import calcular_total, calcular_total_producto


@pytest.fixture
def datos_orden():
    return {
        "precio": 1000,
        "cantidad": 3,
    }


@pytest.mark.parametrize(
    ("precio", "cantidad", "esperado"),
    [
        (100, 2, 200),
        (500, 3, 1500),
        (15000, 1, 15000),
    ],
)
def test_calcular_total(precio, cantidad, esperado):
    assert calcular_total(precio, cantidad) == esperado


@given(
    precio=st.floats(
        min_value=0,
        max_value=1_000_000,
    ),
    cantidad=st.integers(
        min_value=0,
        max_value=1000,
    ),
)
def test_calcular_total_con_hypothesis(precio, cantidad):
    resultado = calcular_total(precio, cantidad)

    assert resultado == precio * cantidad


def test_calcular_total_producto_con_mock():
    consulta_precio = Mock(return_value=1500)

    resultado = calcular_total_producto(
        "Laptop",
        2,
        consulta_precio,
    )

    assert resultado == 3000
    consulta_precio.assert_called_once_with("Laptop")


def test_calcular_total_con_fixture(datos_orden):
    resultado = calcular_total(
        datos_orden["precio"],
        datos_orden["cantidad"],
    )

    assert resultado == 3000
