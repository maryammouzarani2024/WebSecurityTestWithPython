from flask import Flask, jsonify, request, render_template, session, redirect


app = Flask(__name__)
app.secret_key = "change_this_secret_key"   # required for sessions



user_accounts = {
    "alice": {"password": "alice123", "role": "user", "id": 1},
    "bob":   {"password": "bob123",   "role": "user", "id": 2},
    "admin": {"password": "admin123", "role": "admin", "id": 999}
}

# a very simple in-memory "database"
users= {
    1: {"id": 1, "name": "alice", "age": 30},
    2: {"id": 2, "name": "bob", "age": 25}
}

 

def current_user():
    if "username" not in session:
        return None
    return {
        "username": session["username"],
        "role": session["role"],
        "user_id": session["user_id"]
    }


def check_permission(target_user_id):
    user = current_user()
    if not user:
        return None, jsonify({"error": "Not logged in"}), 401

    # admin can access everything
    if user["role"] == "admin":
        return user, None, None

    # normal users can only modify their own data
    if user["user_id"] == target_user_id:
        return user, None, None

    return None, jsonify({"error": "Forbidden: You can only modify your own data"}), 403


# ----------- Regular route to serve index.html -----------
@app.route("/")
def index():
    return render_template("index.html")  # serves an HTML page





#----------- API Endpoints -----------


# login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username not in user_accounts:
        return jsonify({"error": "Invalid username or password"}), 401

    account = user_accounts[username]

    if account["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    # store user in session
    session["username"] = username
    session["role"] = account["role"]
    session["user_id"] = account["id"]

    return jsonify({"message": "Login successful"}), 200


# logout route
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200

 
# get all users information with http://127.0.0.1:5000/api/users
@app.route("/api/users", methods=["GET"])
def get_users():
    user = current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401
    if user["role"] != "admin":
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
    current_user, error, status = check_permission(None)
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

