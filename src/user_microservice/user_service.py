from flask import Flask, jsonify, request

app = Flask(__name__)

users = []
carts = {}

@app.route('/user', methods=['GET'])
def get_users():
    return jsonify({'users': users})

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = {
        'id': len(users) + 1,
        'username': data['username'],
        'email': data['email']
    }
    users.append(new_user)
    carts[new_user['id']] = []  # Create an empty shopping cart for the new user
    return jsonify({'message': 'User created successfully', 'user': new_user}), 201

@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id in carts:
        return jsonify({'user_id': user_id, 'cart': carts[user_id]})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/cart/<int:user_id>', methods=['POST'])
def add_to_cart(user_id):
    data = request.get_json()
    if user_id in carts:
        carts[user_id].append(data)
        return jsonify({'message': 'Item added to the cart', 'user_id': user_id, 'cart': carts[user_id]}), 201
    else:
        return jsonify({'message': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)