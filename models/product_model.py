from database import db


class Product(db.Model):

    product_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    product_name = db.Column(db.String(), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))

    def __init__(self, category_name, category_id):
        self.product_name = category_name
        self.category_id = category_id
