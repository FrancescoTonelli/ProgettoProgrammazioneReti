import socket
import threading

def clientMode():
    print("Client")

def serverMode():
    print("Server")

class MessageColor:
    RED = '\033[91m'
    GREEN = '\033[92m'
    DEFAULT = '\033[0m'

mode = -1
while mode not in ["0", "1"]:
    mode = input(MessageColor.GREEN + "Select mode [" + MessageColor.DEFAULT + 
                "0" + MessageColor.GREEN + ": Server, " + MessageColor.DEFAULT + 
                "1" + MessageColor.GREEN + ": Client]: " + MessageColor.DEFAULT)
    if mode not in ["0", "1"]:
        print(MessageColor.RED + "Non valid input" + MessageColor.DEFAULT)

if(mode == "0"):
    serverMode()
else:
    clientMode()