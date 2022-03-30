from database import db


class Category(db.Model):

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(), nullable=False)
    products = db.relationship('Product', backref='category')

    def __init__(self, category_name):
        self.category_name = category_name
