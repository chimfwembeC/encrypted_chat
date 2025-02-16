import socket
import threading
from encryption import AESCipher
from authentication import authenticate, users

clients = []
key = b'12345678901234567890123456789012'  # AES-256 key should be 32 bytes
cipher = AESCipher(key)

def broadcast(message, sender_socket):
    """Broadcast messages to all clients except the sender"""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, username):
    """Handles communication with a single client"""
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break  # Disconnect if message is empty

            # Prepend username and rebroadcast
            full_message = f"{username}: ".encode() + encrypted_message
            broadcast(full_message, client_socket)
        except:
            break

    print(f"User {username} disconnected.")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    """Starts the chat server"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5555))
    server.listen(5)
    print("Server started on port 5555")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection from {addr}")

        # Receive username
        username = client_socket.recv(1024).decode('utf-8')
        if username not in users or not authenticate(username, users[username]):
            print(f"Authentication failed for {username}")
            client_socket.send("AUTH_FAILED".encode('utf-8'))
            client_socket.close()
            continue

        print(f"User {username} authenticated successfully.")
        clients.append(client_socket)

        # Start handling the client
        thread = threading.Thread(target=handle_client, args=(client_socket, username))
        thread.start()

if __name__ == "__main__":
    start_server()
