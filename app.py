from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS # Import CORS
import json # Used implicitly by request.get_json() but good to have

app = Flask(__name__)
api = Api(app)
CORS(app) # Enable CORS for all routes in your app. This is crucial for Postman.

# In-memory data store (simulating a database for simplicity)
# In a real application, this would be replaced with database interactions (e.g., SQLAlchemy, MongoDB)
users = {
    1: {'name': 'Alice', 'email': 'alice@example.com'},
    2: {'name': 'Bob', 'email': 'bob@example.com'}
}
next_user_id = 3 # To assign unique IDs to new users

# --- Define API Resources (Endpoints) ---

class UserList(Resource):
    def get(self):
        """
        Handles GET requests to /users.
        Returns a list of all users.
        """
        # Convert dictionary values to a list of dictionaries, including the ID
        return [{**user_data, 'id': user_id} for user_id, user_data in users.items()], 200

    def post(self):
        """
        Handles POST requests to /users.
        Creates a new user.
        """
        global next_user_id # Declare global to modify the variable
        new_user_data = request.get_json() # Get JSON data from the request body

        # Basic input validation
        if not new_user_data or 'name' not in new_user_data or 'email' not in new_user_data:
            return {'message': 'Name and email are required fields.'}, 400 # Bad Request

        user_id = next_user_id
        users[user_id] = new_user_data
        next_user_id += 1
        return {**new_user_data, 'id': user_id}, 201 # 201 Created (successful creation)

class User(Resource):
    def get(self, user_id):
        """
        Handles GET requests to /users/<int:user_id>.
        Returns a single user by ID.
        """
        user = users.get(user_id)
        if user:
            return {**user, 'id': user_id}, 200 # OK
        return {'message': 'User not found'}, 404 # Not Found

    def put(self, user_id):
        """
        Handles PUT requests to /users/<int:user_id>.
        Updates an existing user by ID.
        """
        user = users.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404 # Not Found

        updated_data = request.get_json() # Get JSON data for update
        if not updated_data:
            return {'message': 'No data provided for update.'}, 400 # Bad Request

        users[user_id].update(updated_data) # Update existing user data
        return {**users[user_id], 'id': user_id}, 200 # OK

    def delete(self, user_id):
        """
        Handles DELETE requests to /users/<int:user_id>.
        Deletes a user by ID.
        """
        if user_id in users:
            del users[user_id] # Remove user from dictionary
            return '', 204 # 204 No Content (successful deletion with no response body)
        return {'message': 'User not found'}, 404 # Not Found

# --- Add API Resources to the API Router ---
api.add_resource(UserList, '/users') # For /users (GET, POST)
api.add_resource(User, '/users/<int:user_id>') # For /users/{id} (GET, PUT, DELETE)

# --- Run the Flask Application ---
if __name__ == '__main__':
    # app.run(debug=True) is for development.
    # It automatically reloads the server on code changes.
    # For production, set debug=False and use a production-ready WSGI server like Gunicorn.
    app.run(debug=True, port=5001) # Run on port 5001
