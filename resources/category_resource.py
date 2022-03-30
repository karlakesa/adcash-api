from flask import request, jsonify, make_response
from flask_restful import Resource, abort

from database import db
from models.category_model import Category
from schemas.category_schema import CategorySchema
from schemas.product_schema import ProductSchema


class CategoriesResource(Resource):

    @staticmethod
    def get_categories():
        return jsonify(list(CategorySchema().dump(x) for x in Category.query.all())), 200

    @staticmethod
    def post_category():
        data = request.get_json()

        if "category_name" not in data.keys():
            abort(make_response(jsonify(message="Please check the headers!"), 400))
        elif Category.query.filter_by(category_name=data['category_name']).first() is not None:
            abort(make_response(jsonify(message="Category of the same name already exists!"), 400))

        new_category = Category(data['category_name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify(CategorySchema().dump(new_category)), 200

    @staticmethod
    def update_category(category_id):
        data = request.get_json()
        category = Category.query.get(category_id)

        if category is None:
            abort(make_response(jsonify(message="Category not found!"), 400))
        elif "category_name" not in data.keys():
            abort(make_response(jsonify(message="Please check the headers!"), 400))
        elif Category.query.filter_by(category_name=data['category_name']).first() is not None:
            abort(make_response(jsonify(message="Category with the same name already exists!"), 400))

        category.category_name = data['category_name']
        db.session.add(category)
        db.session.commit()
        return jsonify(CategorySchema().dump(category)), 200

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)

        if category is None:
            abort(make_response(jsonify(message="Category not found!"), 400))

        db.session.delete(category)
        db.session.commit()
        return jsonify(CategorySchema().dump(category)), 200

    @staticmethod
    def get_category_by_id(category_id):
        category = Category.query.get(category_id)

        if category is None:
            abort(make_response(jsonify(message="Category does not exist!"), 400))

        return jsonify(CategorySchema().dump(category)), 200

    @staticmethod
    def get_category_products(category_id):
        category = Category.query.get(category_id)

        if category is None:
            abort(make_response(jsonify(message="Category does not exist!"), 400))

        return jsonify(list(ProductSchema().dump(product) for product in category.products)), 200
