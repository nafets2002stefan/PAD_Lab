#Adding path in order to work

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
#Adding path in order to work


from flask import Flask, jsonify, request
from config import *
from models.item import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}?driver={MSSQL_DRIVER}"
db.init_app(app)

# This is a one-time operation to create tables
with app.app_context():
    db.create_all()
items = []

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = [{'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price} for item in items]
    return jsonify({'items': item_list})

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify({'message': 'Item created successfully', 'item': {'id': new_item.id, 'name': new_item.name, 'description': new_item.description, 'price': new_item.price}}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item is not None:
        return jsonify({'item': {'id': item.id, 'name': item.name, 'description': item.description, 'price': item.price}})
    else:
        return jsonify({'message': 'Item not found'}), 404



@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if item is not None:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'message': 'Item not found'}), 404
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
