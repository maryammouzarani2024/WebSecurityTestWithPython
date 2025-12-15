import requests

BASE = "http://127.0.0.1:5000"
session = requests.Session()

print("=== Secure Session Client ===")
# 1. Login
resp = session.post(BASE + "/login", json={
    "username": "alice",
    "password": "alice123"
})
print("LOGIN:", resp.json())

# 2. Get all users
resp = session.get(BASE + "/api/users")
print("USERS:", resp.json())

# 3. Edit Alice's own profile
resp = session.patch(BASE + "/api/users/1", json={"age": 31})
print("PATCH ALICE:", resp.json())

# 4. Try editing Bob (not allowed)
resp = session.patch(BASE + "/api/users/2", json={"age": 99})
print("PATCH BOB:", resp.json())

# 5. Logout
resp = session.post(BASE + "/logout")
print("LOGOUT:", resp.json())
