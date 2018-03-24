from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel
from db import db

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item must have a store id."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # this puts the object in json format
        return {'message': 'Item not found.'}, 404

    def post(self, name):
        #the following if statement is for error control...if item already exists
        if ItemModel.find_by_name(name):
            return {'message': "Item name '{}' already exists in database.".format(name)}, 400 # 400 is 'bad request' code

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)# unpacking 'data['price'], data['store_id']'

        try:
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500 # internal server error code
        return item.json(), 201 # 201 is the 'created' return code # must always return json data

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [x.json() for x in ItemModel.query.all()]}# using list comprehension...more pythonic
                # as a lambda, 'return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}'
