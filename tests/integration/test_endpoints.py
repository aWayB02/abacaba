import uuid
from fastapi.testclient import TestClient
from abacaba.__main__ import app

client = TestClient(app)



def test_create_product_success():
    payload = {"name": "Laptop", "price": 1500}

    response = client.post("/products", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["name"] == "Laptop"
    assert data["price"] == 1500

    uuid.UUID(data["id"])


def test_create_product_missing_name():
    payload = {"price": 1000}

    response = client.post("/products", json=payload)

    assert response.status_code == 400
    assert response.json() == {"error": "Product not found"}


def test_create_product_missing_price():
    payload = {"name": "Laptop"}

    response = client.post("/products", json=payload)

    assert response.status_code == 400
    assert response.json() == {"error": "Product not found"}



def test_get_products_list():
    # создаём один товар
    client.post("/products", json={"name": "Phone", "price": 800})

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0


def test_get_product_by_id_success():
    created = client.post("/products", json={"name": "Tablet", "price": 600})
    product_id = created.json()["id"]

    response = client.get(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Tablet"
    assert data["price"] == 600


def test_get_product_by_id_not_found():
    random_id = str(uuid.uuid4())

    response = client.get(f"/products/{random_id}")

    assert response.status_code == 404
    assert response.json() == {"error": "Product not found"}


def test_delete_product_success():
    created = client.post("/products", json={"name": "Camera", "price": 1200})
    product_id = created.json()["id"]

    response = client.delete(f"/products/{product_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == product_id
    assert data["name"] == "Camera"
    assert data["status"] == "ok"


def test_delete_product_not_found():
    random_id = str(uuid.uuid4())

    response = client.delete(f"/products/{random_id}")

    assert response.status_code == 404
    assert response.json() == {"error": "Product not found"}
