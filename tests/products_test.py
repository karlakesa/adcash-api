import pytest
from app import create_app

TEST_DATABASE_URL = 'sqlite:///test_database.db'


# initialize test app
@pytest.fixture()
def app():
    app = create_app(TEST_DATABASE_URL)
    app.config["TESTING"] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.post("/categories", json={"category_name": "test_category"})
    yield app


@pytest.fixture()
def client(app):
    app.test_client().post("/categories", json={"category_name": "test_category_1"})
    app.test_client().post("/categories", json={"category_name": "test_category_2"})
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_post_product(client):
    response = client.post("/products", json={"product_name": "test_product", "category_id": 1})
    products = client.get("/products")

    assert products.json[0]['product_name'] == "test_product"
    assert response.status_code == 200


def test_post_product_category_does_not_exist(client):
    response = client.post("/products", json={"product_name": "test_product", "category_id": 3})

    assert response.json['message'] == "Category does not exist!"
    assert response.status_code == 400


def test_post_product_name_already_exists(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.post("/products", json={"product_name": "test_product", "category_id": 1})

    assert response.status_code == 400
    assert response.json['message'] == "Product with the same name exists!"


def test_post_product_wrong_headers(client):
    response = client.post("/products", json={"product": "test_product", "category_id": 1})

    assert response.status_code == 400
    assert response.json['message'] == "Please check the headers!"


def test_get_products(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    client.post("/products", json={"product_name": "test_product2", "category_id": 1})
    response = client.get("/products")

    assert len(response.json) == 2
    assert response.status_code == 200


def test_get_product_by_id(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.get("products/1")

    assert response.json['product_name'] == "test_product"
    assert response.status_code == 200


def test_update_product(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.put("/products/1", json={"product_name": "new_name", "category_id": 2})
    product = client.get("/products/1")

    assert response.status_code == 200
    assert product.json['product_name'] == "new_name"
    assert product.json['category_id'] == 2


def test_update_product_name_already_exists(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    client.post("/products", json={"product_name": "test_product2", "category_id": 1})
    response = client.put("/products/1", json={"product_name": "test_product2", "category_id": 1})

    assert response.status_code == 400
    assert response.json['message'] == "Product with the same name already exists!"


def test_update_product_that_doesnt_exist(client):
    response = client.put("/products/1", json={"product_name": "test_product2", "category_id": 1})

    assert response.status_code == 400
    assert response.json['message'] == "Product not found!"


def test_update_product_category_doesnt_exist(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.put("/products/1", json={"product_name": "test_product2", "category_id": 3})

    assert response.status_code == 400
    assert response.json['message'] == "Category does not exist!"


def test_update_product_wrong_headers(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.put("/products/1", json={"product": "test_product", "category": 1})

    assert response.status_code == 400
    assert response.json['message'] == "Please check the headers!"


def test_delete_product(client):
    client.post("/products", json={"product_name": "test_product", "category_id": 1})
    response = client.delete("/products/1")
    product = client.get("/products/1")

    assert product.json['message'] == "Product not found!"
    assert response.status_code == 200


def test_delete_product_that_doesnt_exist(client):
    response = client.delete("/products/1")

    assert response.status_code == 400
    assert response.json['message'] == "Product not found!"
