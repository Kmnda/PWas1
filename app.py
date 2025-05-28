from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS 
import json 

app = Flask(__name__)
api = Api(app)
CORS(app) 

users = {
    1: {'name': 'Alice', 'email': 'alice@example.com'},
    2: {'name': 'Bob', 'email': 'bob@example.com'}
}
next_user_id = 3 


class UserList(Resource):
    def get(self):
        """
        Handles GET requests to /users.
        Returns a list of all users.
        """
       
        return [{**user_data, 'id': user_id} for user_id, user_data in users.items()], 200

    def post(self):
        """
        Handles POST requests to /users.
        Creates a new user.
        """
        global next_user_id 
        new_user_data = request.get_json() 

        
        if not new_user_data or 'name' not in new_user_data or 'email' not in new_user_data:
            return {'message': 'Name and email are required fields.'}, 400 # Bad Request

        user_id = next_user_id
        users[user_id] = new_user_data
        next_user_id += 1
        return {**new_user_data, 'id': user_id}, 201 

class User(Resource):
    def get(self, user_id):
        """
        Handles GET requests to /users/<int:user_id>.
        Returns a single user by ID.
        """
        user = users.get(user_id)
        if user:
            return {**user, 'id': user_id}, 200 
        return {'message': 'User not found'}, 404 

    def put(self, user_id):
        """
        Handles PUT requests to /users/<int:user_id>.
        Updates an existing user by ID.
        """
        user = users.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404 

        updated_data = request.get_json() 
        if not updated_data:
            return {'message': 'No data provided for update.'}, 400 

        users[user_id].update(updated_data) 
        return {**users[user_id], 'id': user_id}, 200 

    def delete(self, user_id):
        """
        Handles DELETE requests to /users/<int:user_id>.
        Deletes a user by ID.
        """
        if user_id in users:
            del users[user_id] 
            return '', 204 
        return {'message': 'User not found'}, 404 


api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<int:user_id>') 


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=5001)
