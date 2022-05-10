
from urllib.request import urlopen
import certifi
import json
from init_db import connect_to_db
import sqlite3

def get_items():
    items = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for row in rows:
            item = {}
            item["id"] = row["id"]
            item["name"] = row["name"]
            item["price"] = row["price"]
            item["quantity"] = row["quantity"]
            items.append(item)

    except:
        items = []

    return items

def preload():
    """Load object from file."""
    gist_raw_url = "https://gist.githubusercontent.com/chamathpali/7cccd0ff8a0338645559e5ed468231fa/raw/3a467ff8807a090cbdbe5e4583b8d07b925a7979/items.json"
    response = urlopen(gist_raw_url, cafile=certifi.where())
    json_response = json.load(response)

    for res in json_response:
        insert_item(res)

    return {"status": True, "message": "successful."}


def insert_item(item):
    inserted_item = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO items (name, price, quantity) VALUES (?, ?, ?)", (item['name'], item['price'], item['quantity']) )
        conn.commit()
        inserted_item = get_item_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_item


def get_item_by_id(item_id):
    item = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE user_id = ?", (item_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        item["id"] = row["id"]
        item["name"] = row["name"]
        item["price"] = row["price"]
        item["quantity"] = row["quantity"]
    except:
        item = {}

    return item

def delete_user(item_id):
    response = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from items WHERE id = ?", (item_id,))
        conn.commit()
        response["status"] = True
        response["message"] = "Item deleted successfully"
    except:
        conn.rollback()
        response["status"] = False
        response["message"] = "Cannot delete item"
    finally:
        conn.close()

    return response