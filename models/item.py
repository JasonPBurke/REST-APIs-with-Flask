from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')# joins the store to the itemModel using the store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price} # dict representing our item

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name limit 1..returns a ItemModel object

    def save_to_db(self): # this takes the place of update AND insert methods that used sqlite3
        db.session.add(self)
        db.session.commit()# can save the commit till after several objects ore added to db (we onlyy have one here)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
