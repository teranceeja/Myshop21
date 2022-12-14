from datetime import datetime
from shop import db, app


class Addproduct(db.Model):
    __seachable__ = ['name', 'desc']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colours = db.Column(db.Text, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand', backref=db.backref('posts', lazy=True))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category', backref=db.backref('posts', lazy=True))

    image_1 = db.Column(db.String(150), nullable=False)
    image_2 = db.Column(db.String(150), nullable=False)
    image_3 = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return '<Addproduct %r>' % self.name


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)



class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    



with app.app_context():
    db.create_all()