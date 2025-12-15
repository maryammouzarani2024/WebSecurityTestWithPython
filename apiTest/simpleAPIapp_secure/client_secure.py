import requests


BASE_URL = "http://localhost:5000/api/users"




API_KEYS = {
    "alice": "alice-key-123",
    "bob": "bob-key-456",
    "admin": "admin-key-999"
}


def make_headers(user):
    return {
        "X-API-Key": API_KEYS[user],
        "Content-Type": "application/json"
    }


# Get all users
def get_all_users(user="alice"):

    print ("Getting all users: /api/users:")
    response= requests.get(BASE_URL, headers=make_headers(user))
    print("status code:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)



# Get a user by ID
def get_user_by_id(user_id, user="alice"):

    print ("\nGet  /api/users/{}:".format(user_id))
    response= requests.get(f"{BASE_URL}/{user_id}", headers=make_headers(user))
    print("status code:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)


def create_new_user(name, age, user="alice"): 
    # Create a new user
    print ("\nPOST  /api/users:")
    new_user_data= {"name": name, "age": age}
    response= requests.post(BASE_URL, json=new_user_data, headers=make_headers(user))
    print("status code:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)


# Update an existing user
def update_existing_user(user_id, name, age, user="alice"):
    print ("\nPUT /api/users/{}:".format(user_id))
    update_user_data= {"name": name, "age": age}
    response= requests.put(f"{BASE_URL}/{user_id}", json=update_user_data, headers=make_headers(user))
    print("status code:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)


def partially_update_user(user_id, age, user="alice"):
    # Partially update an existing user
    print ("\nPATCH /api/users/{}:".format(user_id))
    patch_user_data= {"age": age}
    response= requests.patch(f"{BASE_URL}/{user_id}", json=patch_user_data, headers=make_headers(user))
    print("status code:", response.status_code)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)

# Delete a user with an ID 
def delete_user(user_id, user="alice"):
    print ("\nDELETE /api/users/{}:".format(user_id))
    response= requests.delete(f"{BASE_URL}/{user_id}", headers=make_headers(user))
    print("status code:", response.status_code)
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Response is not valid JSON:")
        print(response.text)
    else:
        print("JSON response:", data)


if __name__== "__main__":
    print("Bob gets user list:")
    print(get_all_users("bob"))

    print("\nBob tries to edit Alice (should fail):")
    print(update_existing_user(1, "Alice", 99, user="bob"))

    print("\nAlice edits her own profile:")
    print(partially_update_user(1, 31, user="alice"))

    print("\nAdmin creates a new user:")
    print(create_new_user("Charlie", 45, user="admin"))

    print("\nAdmin deletes Bob:")
    print(delete_user(2, user="admin"))

