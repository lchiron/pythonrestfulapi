from flask_restful import Resource, reqparse
from models.store import StoreModel


class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name {} already exist".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the store"}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}

    def put(self, name):

        data = Store.parser.parse_args()

        store = StoreModel.find_by_name(name)

        if store:
            store.name = data['name']
        else:
            store = StoreModel(name)

        store.save_to_db()

        return store.json(), 201


class StoreList(Resource):

    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        # return {'stores': [item.json() for item in StoreModel.query.all()]}
        return {'stores': [item.json() for item in StoreModel.query.find_all()]}
