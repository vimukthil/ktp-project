from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(
    app,
    version="1.0",
    title="Item API",
    description="A simple Item API",
)

ns = api.namespace("items", description="Item operations")

item = api.model(
    "Item",
    {
        "id": fields.Integer(readonly=True, description="The item unique identifier"),
        "name": fields.String(required=True, description="The item name"),
        "price": fields.Integer(required=True, description="The price of an item"),
        "quantity": fields.Integer(
            required=True, description="The quantity of an item"
        ),
    },
)


class Item(object):
    def __init__(self):
        self.counter = 0
        self.items = [
            {"id": 1, "name": "W Series Plunger Pump", "price": 3290, "quantity": 100},
            {"id": 2, "name": "Quickflange", "price": 12500, "quantity": 3},
            {
                "id": 3,
                "name": "Solar Chemical Injection Pump",
                "price": 5000,
                "quantity": 5,
            },
        ]


@ns.route("/")
class ItemList(Resource):
    """Shows a list of all items, and lets you POST to add new tasks"""

    item_obj = Item()

    @ns.doc("list_items")
    @ns.marshal_list_with(item)
    def get(self):
        """List all tasks"""
        return self.item_obj.items


if __name__ == "__main__":
    app.run(debug=True)
