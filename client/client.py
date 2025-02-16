import socket
import threading
from encryption import AESCipher
from authentication import authenticate

# Replace with your server's IP address
SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

def receive_messages(client_socket, cipher):
    """Receives and decrypts messages from the server"""
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break  # Exit if connection is lost

            try:
                # Extract username and encrypted message
                username, enc_msg = encrypted_message.split(b": ", 1)

                # Ensure enc_msg is bytes before decrypting
                if isinstance(enc_msg, str):  
                    enc_msg = enc_msg.encode()  

                decrypted_message = cipher.decrypt(enc_msg)  # No need for `.decode()` if already a string

                print(f"\n{username.decode()}: {decrypted_message}")
                print("You: ", end="", flush=True)  # Keep input line clean

            except Exception as e:
                print(f"\nError decrypting message: {e}")

        except:
            print("\nDisconnected from server.")
            client_socket.close()
            break


def send_messages(client_socket, cipher):
    """Sends encrypted messages to the server"""
    while True:
        try:
            message = input("You: ")
            if message.lower() == 'exit':
                print("Disconnecting...")
                client_socket.close()
                break

            encrypted_message = cipher.encrypt(message)
            client_socket.send(encrypted_message)

        except:
            print("\nError sending message.")
            client_socket.close()
            break

def start_client():
    """Starts the chat client"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if not authenticate(username, password):
        print("Authentication failed!")
        return

    key = b'12345678901234567890123456789012'  # AES-256 key should be 32 bytes
    cipher = AESCipher(key)

    print("-" * 50)
    print("Authentication successful!")
    print(f"Hello, {username}!")
    print("-" * 50)

    client_socket.send(username.encode('utf-8'))

    # Start receiving messages in a separate thread
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, cipher), daemon=True)
    receive_thread.start()

    # Start sending messages in the main thread
    send_messages(client_socket, cipher)

if __name__ == "__main__":
    start_client()
