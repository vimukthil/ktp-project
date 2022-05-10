from flask import Flask, request, jsonify
from urllib.request import urlopen
import certifi
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

if __name__ == "__main__":
    app.run(debug=True)
