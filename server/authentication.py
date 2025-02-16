users = {
    "user1": "password1",
    "user2": "password2",
    # More users can be added here
}

def authenticate(username, password):
    """Authenticate user based on username and password"""
    if username in users and users[username] == password:
        return True
    return False
