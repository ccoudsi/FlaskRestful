from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')
    # Here will make the creation of the store faster but accessing the json()
    # method below slower it is a trade off

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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
