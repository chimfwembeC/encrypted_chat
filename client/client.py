# client/client.py
import socket
import threading
from encryption import AESCipher
from authentication import authenticate

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

def receive_messages(client_socket, cipher):
    """Receive and decrypt messages from the server."""
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break  # Connection lost
            # cipher.decrypt returns a string, so no extra decode needed
            decrypted_message = cipher.decrypt(encrypted_message)
            print(f"\n{decrypted_message}")
            print("You: ", end="", flush=True)
        except Exception as e:
            print("\nDisconnected from server.")
            client_socket.close()
            break

def send_messages(client_socket, cipher, username):
    """Encrypt and send messages to the server."""
    while True:
        try:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Disconnecting...")
                client_socket.send(cipher.encrypt("exit"))
                client_socket.close()
                break

            # Join room command: join room <room_key> <room_name>
            if message.startswith("join room"):
                parts = message.split(" ")
                if len(parts) < 4:
                    print("Invalid room join command. Usage: join room <room_key> <room_name>")
                    continue
                room_key, room_name = parts[2], parts[3]
                full_message = f"ROOM:{room_key}:{room_name}"
                client_socket.send(cipher.encrypt(full_message))

            # Private message: private <username> <message>
            elif message.startswith("private"):
                parts = message.split(" ", 2)
                if len(parts) < 3:
                    print("Invalid private message format. Usage: private <username> <message>")
                    continue
                target_username = parts[1]
                private_message = parts[2]
                full_message = f"PRIVATE:{target_username}:{private_message}"
                client_socket.send(cipher.encrypt(full_message))

            # Otherwise, treat as broadcast message
            else:
                full_message = f"BROADCAST:{message}"
                client_socket.send(cipher.encrypt(full_message))

        except Exception as e:
            print("\nError sending message:", e)
            client_socket.close()
            break

def start_client():
    """Start the chat client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not authenticate(username, password):
        print("Authentication failed!")
        client_socket.close()
        return

    # AES key must match the server's key (32 bytes for AES-256)
    key = b'12345678901234567890123456789012'
    cipher = AESCipher(key)

    print("-" * 50)
    print(f"Hello, {username}! Welcome to the chat.")
    print("Type 'exit' to leave the chat.")
    print("-" * 50)

    # Send username (plaintext) to the server
    client_socket.send(username.encode('utf-8'))

    # Start a thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cipher), daemon=True)
    receive_thread.start()

    # Send messages from the main thread
    send_messages(client_socket, cipher, username)

if __name__ == "__main__":
    start_client()
