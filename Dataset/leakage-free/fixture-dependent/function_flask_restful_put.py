from flask import Flask, request
from flask_restful import Api, Resource, fields, marshal_with

class UpdateItem(Resource):
    item_fields = {
        'name': fields.String,
        'price': fields.Float
    }
    @marshal_with(item_fields)
    def put(self, item_id, items):
        item = items.get(item_id)
        if not item:
            return {"message": f"Item with ID {item_id} not found"}, 404

        data = request.get_json()
        item.update({k: v for k, v in data.items() if k in item})
        return item

