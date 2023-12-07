import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import requests
from flask import Flask, jsonify, request
from config import *
from models.user import *
from models.cart import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mssql+pyodbc://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME2}?driver={MSSQL_DRIVER}"
db_user.init_app(app)

with app.app_context():
    db_user.create_all()

carts = {}

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{'id': user.id, 'username': user.username, 'password': user.password} for user in users]
    return jsonify({'users': user_list})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'])
    db_user.session.add(new_user)
    db_user.session.commit()

    return jsonify({'message': 'Item created successfully', 'item': {'id': new_user.id, 'username': new_user.username, 'password': new_user.password}}), 201


@app.route('/user/<int:user_id>/cart', methods=['GET'])
def get_cart(user_id):
    user_cart = Cart.query.filter_by(user_id=user_id).all()
    if user_cart:
        user_name = User.query.get(user_id).username

        item_ids = [cart_item.item_id for cart_item in user_cart]
        items = []
        for item_id in item_ids:
            response = requests.get(f'http://127.0.0.1:5003/items/{item_id}')
            items.append(response.json()['item'])
        return jsonify({'username': user_name, 'items': items})
    else:
        return jsonify({'message': 'User not found or doesn`t have anything in cart.'}), 404

@app.route('/user/<int:user_id>/cart', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    new_cart_item = Cart(user_id=user_id, item_id=data['item_id'])
    
    db_user.session.add(new_cart_item)
    db_user.session.commit()

    return jsonify({'message': 'Item added to the cart', 'user_id': user_id, 'cart_item_id': new_cart_item.id}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)