Here's a `README.md` file for your project that explains the functionality and provides instructions for running and testing the server and client:

```markdown
# Secure Chat Application with AES Encryption

This is a secure chat application that allows multiple users to communicate with each other in rooms. It supports both **private messaging** and **room-based communication**. Messages are encrypted using **AES encryption** for security.

## Features

- **AES Encryption**: All messages sent between clients and the server are encrypted using the AES-256 encryption standard.
- **Authentication**: Users must authenticate with a username and password before being able to join rooms or send messages.
- **Room-based Communication**: Users can create or join rooms, and send messages to all members of a specific room.
- **Private Messaging**: Users can send private messages to other users in the system.
- **Broadcasting**: Messages can be broadcast to everyone in a specific room.
  
## Requirements

- Python 3.x
- `pycryptodome` (for AES encryption)
- `threading` (for handling multiple clients)

### Installing dependencies

To install the required dependencies, you can use the following command:

```bash
pip install pycryptodome
```

## How It Works

### Server

The server handles the following tasks:

* **Authentication**: Verifies users using the `users` dictionary (username and password).
* **Room Management**: Manages rooms where users can send messages to all members of a room.
* **Private Messaging**: Enables users to send private messages to one another.
* **Message Broadcasting**: Sends broadcast messages to all clients in a specific room.

### Client

The client connects to the server and allows the user to:

* Authenticate using a username and password.
* Join or create rooms using a room key and room name.
* Send private messages to other users.
* Send broadcast messages to all users in a room.

## How to Run

### Step 1: Set up the Server

1. Navigate to the server directory.
2. Ensure the server script has access to the `encryption.py` and `authentication.py` files.
3. Run the server script using the following command:

```bash
python server.py
```

The server will start listening on port `5555` for incoming client connections.

### Step 2: Set up the Client

1. Navigate to the client directory.
2. Ensure the client script has access to the `encryption.py` and `authentication.py` files.
3. Run the client script using the following command:

```bash
python client.py
```

### Step 3: Testing

#### Authentication

1. When prompted, enter a **valid username** and **password** to authenticate.
2. If the username or password is invalid, you will be notified that authentication failed.

#### Joining a Room

1. To join a room, enter the following command:

   ```
   join room <room_key> <room_name>
   ```

   Example:

   ```
   join room secretKey room1
   ```
2. If the room exists and the key matches, you will successfully join the room.

#### Sending Private Messages

1. To send a private message to another user, use the following format:

   ```
   private <username> <message>
   ```

   Example:

   ```
   private john Hello, John! How are you?
   ```

   This will send an encrypted private message to the user `john`.

#### Sending Broadcast Messages

1. To send a message to everyone in the room, simply type the message and press Enter. For example:

   ```
   Hello, everyone in the room!
   ```

   This message will be broadcast to everyone in the room you're currently in.

#### Exiting the Chat

1. To exit the chat, type `exit` and press Enter.

## Server Commands

* `ROOM:<room_key>:<room_name>`: Join a room with the specified key and room name.
* `PRIVATE:<username>:<message>`: Send a private encrypted message to the specified user.
* `BROADCAST:<message>`: Send a message to all users in the current room.

## Security

* **AES Encryption**: All messages exchanged between clients and the server are encrypted using AES-256 encryption for confidentiality.
* **Authentication**: The server uses a simple username-password system to authenticate users.

## Example

1. **Start Server**:
   Run the server:

   ```bash
   python server.py
   ```

   The server will be running and listening on port `5555`.
2. **Start Clients**:
   In two separate terminals, run two clients:

   ```bash
   python client.py
   ```
3. **Join Room**:
   In the client prompt, you can join a room:

   ```bash
   join room secretKey room1
   ```
4. **Send Messages**:

   * To send a private message:
     ```bash
     private john Hello, John!
     ```
   * To send a broadcast message:
     ```bash
     Hello, everyone in the room!
     ```

## License

This project is open source and available under the MIT License.

```

### Explanation:

- **Features**: Lists the major functionalities of the chat app.
- **Requirements**: Includes the dependencies needed for the application, along with instructions on installing them.
- **How it Works**: Explains how both the server and the client interact.
- **How to Run**: Provides instructions on how to run both the server and the client.
- **Testing**: Includes instructions for joining rooms, sending private messages, and broadcasting messages.
- **Security**: Outlines the use of AES encryption for secure message transfer.

You can further customize this README according to your preferences or project-specific details.
```
