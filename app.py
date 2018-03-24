from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns off flask_sqlalchemy tracker as SQLAlchemy has a better one built in
app.secret_key = 'aSecretKey'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # creates a new endpiont.. /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')# this Resource is imported from user.py and added to the api here w/an endpoint


if __name__ == '__main__':# this keeps app.py from running if we import it to another file and that file is read
    from db import db # imported here due to 'circular imports'
    db.init_app(app)
    app.run(port=5000, debug=True)
