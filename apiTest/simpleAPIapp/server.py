from flask import Flask, jsonify, request

app=Flask(__name__)

# a very simple in-memory "database"
users= {
    1: {"id": 1, "name": "Alice", "age": 30},
    2: {"id": 2, "name": "Bob", "age": 25}
}

#----------- Rest API Endpoints -----------


# get all users information with http://127.0.0.1:5000/api/users
@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(list(users.values())), 200


# get user information by user id with http://127.0.0.1:5000/api/users/<user_id>
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user= users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "The requested user does not exist."}), 404
    
# create a new user with http://127.0.0.1:5000/api/users
@app.route("/api/users", methods=["POST"])
def create_user():
    data= request.get_json()
    if not data or "name" not in data or "age" not in data:
        return jsonify({"error": "Invalid user data."}), 400    
    new_id= max(users.keys()) + 1 if users else 1
    new_user= {"id": new_id, "name": data["name"], "age": data["age"]}
    users[new_id]= new_user
    return jsonify(new_user), 201   


# update existing user information with http://127.0.0.1:5000/api/users/<user_id>
@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user= users.get(user_id)
    if not user:
        return jsonify({"error": "The requested user does not exist."}), 404    
    data= request.get_json()
    if not data:
        return jsonify({"error": "Invalid user data."}), 400    
    if not all(key in data for key in ("name", "age")):
        return jsonify({"error": "Both 'name' and 'age' fields are required."}), 400
   
    user.update({k: v for k, v in data.items() if k in ["name", "age"]})
    return jsonify(user), 200


# update existing user information partially with http://127.0.0.1:5000/api/users/<user_id>
@app.route("/api/users/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    user= users.get(user_id)
    if not user:
        return jsonify({"error": "The requested user does not exist."}), 404    
    data= request.get_json()
    if not data:
        return jsonify({"error": "Invalid user data."}), 400   
    
    user.update({k: v for k, v in data.items() if k in ["name", "age"]})
    return jsonify(user), 200


# delete a user by user id with http://127.0.0.1:5000/api/users/<user_id>
@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully."}), 200
    else:
        return jsonify({"error": "The requested user does not exist."}), 404
    



if __name__== "__main__":
    app.run(debug=True)

