from flask import Flask
from flask_restful import Api, Resource, reqparse


class UpdateItem(Resource):
    def put(self, item_id, parser, items):
        item = items.get(item_id)
        if not item:
            return {"message": f"Error: Item with ID {item_id} not found"}, 404

        args = parser.parse_args()
        item['name'] = args['name']
        item['price'] = args['price']
        item['quantity'] = args['quantity']

        return item

