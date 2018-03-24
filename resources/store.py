from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200 # 200 is the default code returned so it can be omitted
        return {'message': "Store called '{}' not found".format(name)}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store named '{}' already exists.".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occured trying to save store to the database'}, 500
        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'An error occured when attempting to delete the store.'}, 500
            return {'message': 'Store Deleted.'}, 200

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
