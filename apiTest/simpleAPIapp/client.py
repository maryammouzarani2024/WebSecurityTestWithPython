import requests

BASE_URL = "http://localhost:5000/api/users"


# Get all users
print ("Getting all users: /api/users:")
response= requests.get(BASE_URL)
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)



# Get a user by ID
print ("\nGet  /api/users/1:")
response= requests.get(f"{BASE_URL}/1")
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)

# Create a new user
print ("\nPOST  /api/users:")
new_user_data= {"name": "David", "age": 28}
response= requests.post(BASE_URL, json=new_user_data)
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)


# Update an existing user
print ("\nPUT /api/users/2:")
update_user_data= {"name": "Robert", "age": 26}
response= requests.put(f"{BASE_URL}/2", json=update_user_data)
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)

# Partially update an existing user
print ("\nPATCH /api/users/1:")
patch_user_data= {"age": 31}
response= requests.patch(f"{BASE_URL}/1", json=patch_user_data)
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)


# Delete a user with an ID 
print ("\nDELETE /api/users/3:")
response= requests.delete(f"{BASE_URL}/3")
print("status code:", response.status_code)

try:
    data = response.json()
except requests.exceptions.JSONDecodeError:
    print("Response is not valid JSON:")
    print(response.text)
else:
    print("JSON response:", data)
