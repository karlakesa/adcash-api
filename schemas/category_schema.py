from marshmallow import Schema, fields


class CategorySchema(Schema):

    category_id = fields.Integer()
    category_name = fields.String()
