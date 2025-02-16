users = {
    "user1": "password1",
    "user2": "password2"
}

def authenticate(username, password):
    return username in users and users[username] == password