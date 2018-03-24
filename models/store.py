from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [x.json() for x in self.items.all()]} # dict representing our item

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name limit 1..returns a ItemModel object

    def save_to_db(self): # this takes the place of update AND insert methods that used sqlite3
        db.session.add(self)
        db.session.commit()# can save the commit till after several objects ore added to db (we onlyy have one here)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
