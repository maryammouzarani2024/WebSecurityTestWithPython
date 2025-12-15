from flask import Flask, jsonify, request, render_template

app=Flask(__name__)

# a very simple in-memory "database"
users= {
    1: {"id": 1, "name": "Alice", "age": 30},
    2: {"id": 2, "name": "Bob", "age": 25}
}


API_KEYS = {
    "alice-key-123": "Alice",
    "bob-key-456": "Bob",
    "admin-key-999": "Admin"
}

# User roles
USER_ROLES = {
    "Alice": "user",
    "Bob": "user",
    "Admin": "admin"
}


def get_current_user():
    api_key = request.headers.get("X-API-Key")
    if not api_key or api_key not in API_KEYS:
        return None, jsonify({"error": "Unauthorized"}), 401
    
    username = API_KEYS[api_key]
    role = USER_ROLES[username]
    return {"username": username, "role": role}, None, None

def check_permission(target_user_id):
    current_user, error, status = get_current_user()
    if error:
        return None, error, status

    # Admin can do everything
    if current_user["role"] == "admin":
        return current_user, None, None

    # Normal users can access ONLY their own user id
    if current_user["role"] == "user":
        if current_user["username"].lower() == users[target_user_id]["name"].lower():
            return current_user, None, None
        else:
            return None, jsonify({"error": "Forbidden: you can only modify your own data."}), 403


# ----------- Regular route to serve index.html -----------
@app.route("/")
def index():
    return render_template("index.html")  # serves an HTML page


#----------- API Endpoints -----------


# get all users information with http://127.0.0.1:5000/api/users
@app.route("/api/users", methods=["GET"])
def get_users():
    current_user, error, status = get_current_user()
    if error:
        return error, status
    if current_user["role"] != "admin":
        return jsonify({"error": "Forbidden: only admin can access all users."}), 403
    return jsonify(list(users.values())), 200


# get user information by user id with http://127.0.0.1:5000/api/users/<user_id>
@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    current_user, error, status = check_permission(user_id)
    if error:
        return error, status

    user= users.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "The requested user does not exist."}), 404
    
# create a new user with http://127.0.0.1:5000/api/users
@app.route("/api/users", methods=["POST"])
def create_user():
    current_user, error, status = get_current_user()
    if error:
        return error, status
    if current_user["role"] != "admin":
        return jsonify({"error": "Forbidden: only admin can create new users."}), 403
    
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
    current_user, error, status = check_permission(user_id)
    if error:
        return error, status

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
    current_user, error, status = check_permission(user_id)
    if error:
        return error, status
    
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
    current_user, error, status = check_permission(user_id)
    if error:   
        return error, status
    
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully."}), 200
    else:
        return jsonify({"error": "The requested user does not exist."}), 404
    



if __name__== "__main__":
    app.run(debug=True)

