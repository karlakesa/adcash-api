from flask import Flask
from database import db

from resources.category_resource import CategoriesResource
from resources.product_resource import ProductsResource


def create_app(database_uri):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.init_app(app)

    @app.before_first_request
    def create_table():
        if app.config['TESTING'] is True:
            db.drop_all()
        db.create_all()

    @app.route('/')
    def home():
        return "AdCash api test application"

    # CATEGORY ROUTES START

    @app.route('/categories', methods=["GET"])
    def get_categories():
        return CategoriesResource.get_categories()

    @app.route('/categories', methods=["POST"])
    def post_category():
        return CategoriesResource.post_category()

    @app.route('/categories/<category_id>', methods=["PUT"])
    def update_category(category_id):
        return CategoriesResource.update_category(category_id)

    @app.route('/categories/<category_id>', methods=["DELETE"])
    def delete_category(category_id):
        return CategoriesResource.delete_category(category_id)

    @app.route('/categories/<category_id>/products', methods=["GET"])
    def get_category_products(category_id):
        return CategoriesResource.get_category_products(category_id)

    @app.route('/categories/<category_id>', methods=["GET"])
    def get_category_by_id(category_id):
        return CategoriesResource.get_category_by_id(category_id)

    # PRODUCT ROUTES START

    @app.route('/products', methods=["GET"])
    def get_products():
        return ProductsResource.get_products()

    @app.route('/products', methods=["POST"])
    def post_product():
        return ProductsResource.post_product()

    @app.route('/products/<product_id>', methods=["PUT"])
    def update_product(product_id):
        return ProductsResource.update_product(product_id)

    @app.route('/products/<product_id>', methods=["DELETE"])
    def delete_product(product_id):
        return ProductsResource.delete_product(product_id)

    @app.route('/products/<product_id>', methods=["GET"])
    def get_product_by_id(product_id):
        return ProductsResource.get_product_by_id(product_id)

    return app


if __name__ == '__main__':
    create_app('sqlite:///database.db').run()
