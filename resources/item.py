from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    # added a Class variable "parser" here so we don't duplicate code in the post() & put()
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id.")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()  # return dictionary can not return object
        return{'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with '{}' already exists." .format(name)}, 400

        data = Item.parser.parse_args()  # Now will only provide the data that match our parser
        # item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])
        # item = ItemModel(name, **data) ==> same as above

        try:
            item.save_to_db()
        except Exception:
            return {"message": "An error occurred inserting the item."}, 500
            # Internal Server Error

        return item.json(), 201  # 201 status code = created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return{'message': 'Item deleted'}

    def put(self, name):  # Update item or create one if doesn't exists
        data = Item.parser.parse_args()  # Now will only provide the data that match our parser
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
            # item = ItemModel(name, **data) ==> same as above
        else:
            item.price = data['price']
            # you can also change the store id here

        item.save_to_db()  # because item has a unique id now
        return item.json()


class ItemList(Resource):
    def get(self):
        # using list comprehension in Python only
        return {'items': [item.json() for item in ItemModel.query.all()]}
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}  # using Lambda
