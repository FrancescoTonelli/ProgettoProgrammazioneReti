import socket
import threading

def client_receive(client_socket):
    """
    Receives messages from the server and prints them to the client's console.

    Args:
        client_socket (socket.socket): The client's socket connection.

    Returns:
        None
    """
    while True:
        try:
            print(client_socket.recv(BUFFER_SIZE).decode())
        except:
            break
            

def client_send(client_socket):
    """
    Sends messages from the client to the server.

    Args:
        client_socket (socket.socket): The client's socket connection.

    Returns:
        None
    """
    while True:
        try:
            message = input()
            client_socket.send(message.encode())
        except:
            break

def client_mode():
    """
    Manages the client-side functionality, like connecting to the server,
    sending and receiving messages, and handling exceptions.

    Args:
        None

    Returns:
        None
    """
    try:
        host = input("Insert host server's IP: ")
        port = input("Insert host server's port: ")
        
        if not host:
            host = HOST
        
        if not port:
            port = PORT
        else:
            port = int(port)
        
        this_socket.connect((host, port))
        send_thread = threading.Thread(target=client_send, args=(this_socket,))
        send_thread.start()
        client_receive(this_socket)
        send_thread.join()
        print("---Server disconnected---")
        this_socket.close()
        client_mode()
    except Exception as e:
        print(e)

def server_broadcast(message, sender=None):
    """
    Broadcasts a message to all connected users in the server.

    Args:
        message (str): The message to be broadcasted.
        sender (socket.socket, optional): The socket of the sender. Defaults to None.

    Returns:
        None
    """
    if sender is None:
        print(message)
    else:
        print(f"{users[sender]}: {message}")
    
    for u in users:
        if u != sender:
            if sender is None:
                u.send(message.encode())
            else:
                u.send((f"{users[sender]}: {message}").encode())

def server_user_manager(user):
    """
    Manages a user's connection to the server, including handling the user's
    username, sending and receiving messages, and broadcasting user activities.

    Args:
        user (socket.socket): The socket connection of the user.

    Returns:
        None
    """
    try:
        username = user.recv(BUFFER_SIZE).decode()
        users[user] = username
        server_broadcast(f"---{username} enter the chat---")
    except:
        user.close()
        return
    
    while True:
        try:
            server_broadcast(user.recv(BUFFER_SIZE).decode(), user)
        except:
            break
    
    del users[user]
    server_broadcast(f"---{username} left the chat---")
    user.close()
    

def server_mode():
    """
    Manages the server-side functionality, including binding to a host and port,
    listening for incoming connections, and handling user connections with threads.

    Args:
        None

    Returns:
        None
    """
    global users
    users = {}
    try:
        this_socket.bind((HOST, PORT))
    except:
        print("It's possible to create only one server at a time on the same host and port")
        mode_selector()
    print(f"Server on {HOST}:{PORT}")
    this_socket.listen()
    while True:
        user, user_address = this_socket.accept()
        user.send(("Insert your username").encode())
        threading.Thread(target=server_user_manager, args=(user,)).start()

def mode_selector():
    """
    Allows the user to select whether to run the program as a server (0) or client (1).

    Args:
        None

    Returns:
        None
    """
    mode = -1
    while mode not in ["0", "1"]:
        mode = input("Select mode [0: Server, 1: Client]: ")
        if mode not in ["0", "1"]:
            print("Non valid input")

    if(mode == "0"):
        server_mode()
    else:
        client_mode()

# Configuration
HOST = socket.gethostbyname(socket.gethostname())
PORT = 53000
BUFFER_SIZE = 1024

if __name__ == "__main__":
    this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mode_selector()

