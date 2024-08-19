from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.item import ItemModel

BLANK_ERROR = "'{}' cannot be blank."
NAME_ALREADY_EXISTS = "An item with name '{}' already exists."
ERROR_INSERTING = "An error occurred while inserting the item."
ITEM_NOT_FOUND = "Item not found."
ITEM_DELETED = "Item deleted."


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price", type=float, required=True, help=BLANK_ERROR.format("price")
    )
    parser.add_argument(
        "store_id", type=int, required=True, help=BLANK_ERROR.format("store_id")
    )

    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return {"message": NAME_ALREADY_EXISTS.format(name)}, 400

        data = cls.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": ERROR_INSERTING}, 500

        return item.json(), 201

    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}, 200
        return {"message": ITEM_DELETED}, 404

    @classmethod
    def put(cls, name: str):
        data = cls.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data["price"]
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 200


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {"items": [item.json() for item in ItemModel.find_all()]}, 200
