import pytest
from app import create_app

TEST_DATABASE_URL = 'sqlite:///test_database.db'


# initialize test app
@pytest.fixture()
def app():
    app = create_app(TEST_DATABASE_URL)
    app.config["TESTING"] = True
    app.config['WTF_CSRF_ENABLED'] = False

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_post_category(client):
    response = client.post("/categories", json={"category_name": "test_category"})
    categories = client.get("categories")

    assert categories.json[0]["category_name"] == "test_category"
    assert response.status_code == 200


def test_post_category_wrong_headers(client):
    response = client.post("/categories", json={"category_na": "test_category"})

    assert response.json['message'] == "Please check the headers!"
    assert response.status_code == 400


def test_post_category_name_already_exists(client):
    client.post("/categories", json={"category_name": "name_exists"})
    response = client.post("/categories", json={"category_name": "name_exists"})

    assert response.json['message'] == "Category of the same name already exists!"
    assert response.status_code == 400


def test_get_categories(client):
    response = client.get("/categories")

    assert response.status_code == 200


def test_get_category_by_id(client):
    client.post("/categories", json={"category_name": "test_category"})
    response = client.get("categories/1")

    assert response.status_code == 200


def test_update_category(client):
    client.post("/categories", json={"category_name": "test_category"})
    client.put("/categories/1", json={"category_name": "new_name"})
    category = client.get("categories/1")

    assert category.json['category_name'] == "new_name"


def test_update_category_that_does_not_exist(client):
    client.post("/categories", json={"category_name": "test_category"})
    response = client.put("/categories/2", json={"category_name": "new_name"})

    assert response.json['message'] == "Category not found!"
    assert response.status_code == 400


def test_update_category_name_already_exists(client):
    client.post("/categories", json={"category_name": "test_category"})
    client.post("/categories", json={"category_name": "test_category2"})
    response = client.put("/categories/2", json={"category_name": "test_category"})

    assert response.json['message'] == "Category with the same name already exists!"
    assert response.status_code == 400


def test_update_category_wrong_headers(client):
    client.post("/categories", json={"category_name": "test_category"})
    response = client.put("/categories/1", json={"category": "new_name"})

    assert response.status_code == 400
    assert response.json['message'] == "Please check the headers!"


def test_get_all_products_of_a_category(client):
    client.post("/categories", json={"category_name": "tools"})
    client.post("/products", json={"product_name": "drill", "category_id": 1})
    client.post("/products", json={"product_name": "hammer", "category_id": 1})
    response = client.get("/categories/1/products")
    category_id_does_not_exist = client.get("/categories/2/products")

    assert response.json[0]['product_name'] == "drill"
    assert response.json[1]['product_name'] == "hammer"
    assert response.status_code == 200
    assert category_id_does_not_exist.json['message'] == "Category does not exist!"


def test_delete_category(client):
    client.post("/categories", json={"category_name": "category_to_delete"})
    response = client.delete("/categories/1")
    category = client.get("/categories/1")

    assert category.status_code == 400
    assert response.status_code == 200


def test_delete_category_not_found(client):
    client.post("/categories", json={"category_name": "category_to_delete"})
    response = client.delete("/categories/2")

    assert response.json["message"] == "Category not found!"
    assert response.status_code == 400
