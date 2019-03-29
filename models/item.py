from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # return ItemModel.query.filter_by(name=name).first()
        # SELECT * FROM items WHERE name=name LIMIT 1
        # return item model object

    # We can insert and update in one method
    def save_to_db(self):
        db.session.add(self)  # "session" is a collection of objects going to write to DB
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)  # "session" is a collection of objects going to delted to DB
        db.session.commit()
