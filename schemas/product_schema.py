from marshmallow import Schema, fields


class ProductSchema(Schema):

    product_id = fields.Integer()
    product_name = fields.String()
    category_id = fields.Integer()
