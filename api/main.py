from flask import Flask, request, jsonify
from flask_cors import CORS
from init_db import create_db_table
import service


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# prepare the database
create_db_table()

@app.route('/items', methods=['GET'])
def api_get_items():
    return jsonify(service.get_items())

@app.route('/items',  methods = ['POST'])
def api_add_item():
    item = request.get_json()
    return jsonify(service.insert_item(item))

@app.route('/items/preload', methods=['GET'])
def api_preload_db():
    return service.preload()

@app.route('/items/<item_id>',  methods = ['DELETE'])
def api_delete_item(item_id):
    return jsonify(service.delete_item(item_id))

if __name__ == "__main__":
    app.run(debug=True)
