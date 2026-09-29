from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def obtener_token() -> str:
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_inicio():
    response = client.get("/")

    assert response.status_code == 200


def test_login():
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "123456",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_crear_order():
    token = obtener_token()

    response = client.post(
        "/orders/",
        json={
            "product": "Laptop",
            "quantity": 2,
            "price": 15000,
        },
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["product"] == "Laptop"
    assert data["quantity"] == 2
    assert data["price"] == 15000


def test_obtener_orders():
    token = obtener_token()

    response = client.get(
        "/orders/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
