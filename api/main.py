from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from urllib.request import urlopen
import certifi


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
        self.items = []

    def create(self, data):
        item = data
        item["id"] = self.counter = self.counter + 1
        self.items.append(item)
        return item

    def preload(self):
        """Load object from file."""
        gist_raw_url = "https://gist.githubusercontent.com/chamathpali/7cccd0ff8a0338645559e5ed468231fa/raw/3a467ff8807a090cbdbe5e4583b8d07b925a7979/items.json"
        response = urlopen(gist_raw_url, cafile=certifi.where())
        json_response = json.load(response)

        for res in json_response:
            self.create(res)

        return {"status": True, "message": "successful."}


item_obj = Item()


@ns.route("/")
class ItemList(Resource):
    """Shows a list of all items, and lets you POST to add new tasks."""

    @ns.doc("list_items")
    @ns.marshal_list_with(item)
    def get(self):
        """List all tasks"""
        return item_obj.items


@ns.route("/preload")
class ItemAction(Resource):
    """Load list of items."""

    @ns.doc("load_items")
    def get(self):
        item_obj.preload()


if __name__ == "__main__":
    app.run(debug=True)
