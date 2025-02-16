# client/client.py

def authenticate(username, password):
    # This is a simple example. In a real application, you would check the username and password against a database or other secure storage.
    valid_users = {
        "user1": "password1",
        "user2": "password2"
    }
    return valid_users.get(username) == password
