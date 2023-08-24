from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Initialize the MongoClient
client = MongoClient('localhost', 27017)

# Access the "userbase" database
db = client['userbase']

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def index():
    return "Hi guys"


@app.route('/users', methods=['GET'])
def users_list():
    users_collection = db['users']
    users = users_collection.find({})
    output = []
    for user in users:
        output.append({
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
        })
    return jsonify({'result': output})


@app.route('/users', methods=['POST'])
def register():
    data = request.json
    id = data['id']
    username = data['username']
    email = data['email']
    password = data['password']

    user = {
        'id': id,
        'username': username,
        'email': email,
        'password': password
    }
    users_collection = db['users']
    users_collection.insert_one(user)

    return jsonify(message='User registered successfully'), 201


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    try:
        # Convert the string id to a MongoDB ObjectId
        object_id = ObjectId(id)
        users_collection = db['users']
        user = users_collection.find_one({'_id': object_id})

        if user:
            output = {
                'id': str(user['_id']),  # Convert ObjectId back to string
                'username': user['username'],
                'email': user['email'],
                # 'password': user['password']
                # Add other user attributes here
            }
            return output
        else:
            return None  # Return None if user not found
    except Exception as e:
        return str(e)  # Return the error message


@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    try:
        # Convert the string id to a MongoDB ObjectId
        object_id = ObjectId(id)
        users_collection = db['users']
        data = request.json
        users_collection.update_one({'_id': object_id}, {'$set': data})
        return jsonify(message='User updated successfully'), 200
    except Exception as e:
        return str(e)  # Return the error message


@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        # Convert the string id to a MongoDB ObjectId
        object_id = ObjectId(id)
        users_collection = db['users']
        users_collection.delete_one({'_id': object_id})
        return jsonify(message='User deleted successfully'), 200
    except Exception as e:
        return str(e)
