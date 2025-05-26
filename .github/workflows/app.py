from flask import Flask, request, jsonify

app = Flask(__name__)

# Fake DB
users = []

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    users.append(data)
    return jsonify({'msg': 'User added', 'user': data}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
