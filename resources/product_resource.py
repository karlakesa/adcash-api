from flask import request, jsonify, make_response
from flask_restful import Resource, abort

from database import db
from models.product_model import Product
from models.category_model import Category
from schemas.product_schema import ProductSchema


class ProductsResource(Resource):

    @staticmethod
    def get_products():

        return jsonify(list(ProductSchema().dump(x) for x in Product.query.all())), 200

    @staticmethod
    def post_product():
        data = request.get_json()

        if "category_id" not in data.keys() or "product_name" not in data.keys():
            abort(make_response(jsonify(message="Please check the headers!"), 400))
        elif Category.query.filter_by(category_id=data['category_id']).first() is None:
            abort(make_response(jsonify(message="Category does not exist!"), 400))
        elif Product.query.filter_by(product_name=data['product_name']).first() is not None:
            abort(make_response(jsonify(message="Product with the same name exists!"), 400))

        new_category = Product(data['product_name'], data['category_id'])
        db.session.add(new_category)
        db.session.commit()

        return jsonify(ProductSchema().dump(new_category)), 200

    @staticmethod
    def update_product(product_id):
        data = request.get_json()
        product = Product.query.get(product_id)

        if "category_id" not in data.keys() or "product_name" not in data.keys():
            abort(make_response(jsonify(message="Please check the headers!"), 400))
        elif product is None:
            abort(make_response(jsonify(message="Product not found!"), 400))
        elif Product.query.filter_by(product_name=data['product_name']).first() is not None \
                and Product.query.filter_by(product_name=data['product_name']) \
                .first().product_name != product.product_name:
            abort(make_response(jsonify(message="Product with the same name already exists!"), 400))
        elif Category.query.filter_by(category_id=data['category_id']).first() is None:
            abort(make_response(jsonify(message="Category does not exist!"), 400))

        product.product_name = data['product_name']
        product.category_id = data['category_id']
        db.session.add(product)
        db.session.commit()

        return jsonify(ProductSchema().dump(product)), 200

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)

        if product is None:
            abort(make_response(jsonify(message="Product not found!"), 400))

        db.session.delete(product)
        db.session.commit()

        return jsonify(ProductSchema().dump(product)), 200

    @staticmethod
    def get_product_by_id(product_id):
        category = Product.query.get(product_id)
        category_json = ProductSchema().dump(category)

        if not category_json:
            abort(make_response(jsonify(message="Product not found!"), 400))

        return jsonify(category_json), 200
