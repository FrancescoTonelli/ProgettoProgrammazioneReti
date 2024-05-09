import socket
import threading
import tkinter as tk
import datetime

def client_closing_window():
    """
    Closes the client application window and restarts the client mode.
    """
    window.client_socket.close()
    window.destroy()
    print("---Window closed---")
    client_mode()
            
def client_generate_window(client_socket):
    """
    Generates and displays the client application window.

    Args:
        client_socket: The client socket used for communication with the server.
    """
    global window
    window = tk.Tk()
    window.title("Chat_Lab")
    
    message_frame = tk.Frame(window)
    message_frame.pack()
    
    scrollbar = tk.Scrollbar(message_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    message_list = tk.Listbox(message_frame, height=15, width=50, font=("Arial", 12), yscrollcommand=scrollbar.set)
    message_list.pack(side=tk.LEFT, fill=tk.BOTH)
    window.message_list = message_list
    
    scrollbar.config(command=message_list.yview)
    
    instruction_label = tk.Label(window, text="Insert your message here and press enter", font=("Arial", 10), fg="gray")
    instruction_label.pack()
    
    entry_field = tk.Entry(window)
    entry_field.pack(fill=tk.BOTH, padx=10, pady=10)
    entry_field.bind("<Return>", lambda event: client_send())
    window.entry_field = entry_field
    
    window.client_socket = client_socket
    
    window.protocol("WM_DELETE_WINDOW", client_closing_window)

def client_receive():
    """
    Receives messages from the client socket and displays them in the application window.
    """
    while True:
        try:
            message = window.client_socket.recv(BUFFER_SIZE).decode()
            window.message_list.insert(tk.END, message)
            window.message_list.yview(tk.END)
        except:
            break

def client_send():
    """
    Sends a message to the server using the client socket and displays it in the application window.
    """
    try:
        message = window.entry_field.get()
        message += " [ " + datetime.datetime.now().strftime("%H:%M") + " ]"
        if message:
            window.message_list.insert(tk.END, f"You: {message}")
            window.entry_field.delete(0, tk.END)
            window.message_list.yview(tk.END)
            window.client_socket.send(message.encode())
    except:
        print("---Server disconnected---")
        client_closing_window()
        return


def client_mode():
    """
    Manages the client-side functionality, including connecting to the server, handling username input, 
    and initialing send/receive functions and window 
    """
    try:
        this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = ""
        port = ""
        try:
            host = input("Insert host server's IP: ")
            port = input("Insert host server's port: ")
        except: 
            pass
        
        if not host:
            host = HOST
        
        if not port:
            port = PORT
        else:
            port = int(port)
        
        try:
            this_socket.connect((host, port))
        except:
            print("---Connection error---")
            client_mode()
        
        name = ""
        while not name:
            try:
                name = input("Insert your username: ")
                this_socket.send(name.encode())
            except: 
                pass
        
        client_generate_window(this_socket)
        
        thread_receive = threading.Thread(target=client_receive)
        thread_receive.start()
        
        window.mainloop()  
        
        this_socket.close()
        client_mode()
    except Exception as e:
        print(e)
        window.destroy()
        client_mode()

def server_broadcast(message, sender=None):
    """
    Broadcasts a message to all connected users in the server.

    Args:
        message (str): The message to be broadcasted.
        sender (socket.socket, optional): The socket of the sender. Defaults to None.
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
        except KeyboardInterrupt:
            break
        except:
            break
    del users[user]
    server_broadcast(f"---{username} left the chat---")
    user.close()
     

def server_mode():
    """
    Manages the server-side functionality, including binding to a host and port,
    listening for incoming connections, and handling user connections with threads.
    """
    this_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        threading.Thread(target=server_user_manager, args=(user,)).start()

def mode_selector():
    """
    Allows the user to select whether to run the program as a server (0) or client (1).
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

# Configuration settings
HOST = socket.gethostbyname(socket.gethostname())
PORT = 53000
BUFFER_SIZE = 1024

if __name__ == "__main__":
    mode_selector()

