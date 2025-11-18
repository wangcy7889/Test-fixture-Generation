from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
db = SQLAlchemy(app)


class ItemModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)


class Item(Resource):
    resource_fields = {
        'name': fields.String,
        'price': fields.Float,
        'quantity': fields.Integer
    }

    @marshal_with(resource_fields)
    def get(self, item_id):
        item = ItemModel.query.get(item_id)
        if not item:
            return {"message": f"Item with ID {item_id} not found"}, 404
        return item
