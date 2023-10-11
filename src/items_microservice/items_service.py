from flask import Flask, jsonify, request

app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({'items': items})

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = {
        'id': len(items) + 1,
        'name': data['name'],
        'description': data['description'],
        'price': data['price']
    }
    items.append(new_item)
    return jsonify({'message': 'Item created successfully', 'item': new_item}), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is not None:
        return jsonify({'item': item})
    else:
        return jsonify({'message': 'Item not found'}), 404


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is not None:
        items.remove(item)
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'message': 'Item not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
