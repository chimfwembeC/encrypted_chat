# server/server.py
import socket
import threading
from encryption import AESCipher
from authentication import authenticate, users

# Dictionary to store client sockets mapped to a tuple: (username, current_room)
clients = {}
# Predefined rooms with their keys
rooms = {
    "chatroom1": "secretkey1",
    "chatroom2": "secretkey2",
    "chatroom3": "secretkey3",
}

# Shared AES key (32 bytes for AES-256)
key = b'12345678901234567890123456789012'
cipher = AESCipher(key)

def broadcast_to_room(room_name, message, sender_socket):
    """Broadcast message to everyone in a specific room (except sender)."""
    for client_socket, (username, room) in clients.items():
        if room == room_name and client_socket != sender_socket:
            try:
                client_socket.send(cipher.encrypt(message))
            except Exception as e:
                print(f"Error sending message to {username}: {e}")
                client_socket.close()
                clients.pop(client_socket, None)

def find_target_socket(target_username):
    """Find the socket associated with the given username."""
    for client_socket, (username, room) in clients.items():
        if username == target_username:
            return client_socket
    return None

def handle_client(client_socket):
    """Handle communication with a connected client."""
    try:
        # Receive the username (sent in plaintext by the client)
        username_bytes = client_socket.recv(1024)
        if not username_bytes:
            raise ValueError("No data received from client.")
        username = username_bytes.decode('utf-8')

        # For this example, we assume that if the username exists, it is authenticated.
        # (The password was already checked on the client side.)
        if username not in users:
            print(f"Authentication failed for {username}")
            client_socket.send(cipher.encrypt("Authentication failed."))
            client_socket.close()
            return

        # Add client with no room initially.
        clients[client_socket] = (username, None)
        print(f"{username} connected.")

        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                raise ValueError("No message received from client.")
            # Decrypt incoming message
            message = cipher.decrypt(encrypted_message)

            if message.startswith('ROOM:'):
                # Format: ROOM:<room_key>:<room_name>
                parts = message.split(':')
                if len(parts) < 3:
                    client_socket.send(cipher.encrypt("Invalid room join command."))
                    continue
                room_key, room_name = parts[1], parts[2]
                if room_name in rooms and rooms[room_name] == room_key:
                    clients[client_socket] = (username, room_name)
                    client_socket.send(cipher.encrypt(f"Joined room: {room_name}"))
                else:
                    client_socket.send(cipher.encrypt("Invalid room key."))

            elif message.startswith('CREATE ROOM:'):
                # Format: CREATE ROOM:<room_key>:<room_name>
                parts = message.split(':')
                if len(parts) < 3:
                    client_socket.send(cipher.encrypt("Invalid room creation command."))
                    continue
                room_key, room_name = parts[1], parts[2]
                if room_name not in rooms:
                    rooms[room_name] = room_key
                    client_socket.send(cipher.encrypt(f"Room '{room_name}' created."))
                else:
                    client_socket.send(cipher.encrypt(f"Room '{room_name}' already exists."))

            elif message.startswith('PRIVATE:'):
                # Format: PRIVATE:<target_username>:<message>
                parts = message.split(':', 2)
                if len(parts) < 3:
                    client_socket.send(cipher.encrypt("Invalid private message command."))
                    continue
                target_username = parts[1]
                private_message = parts[2]
                target_socket = find_target_socket(target_username)
                if target_socket:
                    target_socket.send(cipher.encrypt(f"Private message from {username}: {private_message}"))
                else:
                    client_socket.send(cipher.encrypt("User not found."))

            elif message.startswith('BROADCAST:'):
                # Format: BROADCAST:<message>
                room_name = clients[client_socket][1]
                if room_name:
                    broadcast_message = message.split(':', 1)[1]
                    broadcast_to_room(room_name, f"{username}: {broadcast_message}", client_socket)
                else:
                    client_socket.send(cipher.encrypt("You are not in any room."))

            elif message == 'exit':
                client_socket.send(cipher.encrypt("Goodbye!"))
                break

            else:
                client_socket.send(cipher.encrypt("Invalid command."))

    except Exception as e:
        print(f"Error handling message from {username}: {e}")
        try:
            client_socket.send(cipher.encrypt("An error occurred. Please try again later."))
        except:
            pass
    finally:
        print(f"Closing connection with {username}")
        client_socket.close()
        clients.pop(client_socket, None)

def kick_user(target_username):
    """Kick a user from the chat."""
    for client_socket, (username, room) in list(clients.items()):
        if username == target_username:
            client_socket.send(cipher.encrypt("You have been kicked out of the room."))
            client_socket.close()
            clients.pop(client_socket, None)
            break

def start_server():
    """Start the server and listen for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server started on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
