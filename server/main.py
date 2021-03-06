#!/usr/bin/python3

import socket 
import select 
import sys
import re
from thread import *
import traceback

class Client:
    def __init__(self, conn, name, channel):
        self.conn = conn
        self.name = name
        self.channel = channel

class Channel:
    def __init__(self, name):
        self.name = name

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
  
# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 
  
# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 
  
""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port)) 
  
""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100) 
  
list_of_clients = [] 
list_of_channels = [Channel("general")]
  
def setUsername(conn, username):
    for client in list_of_clients:
        if client.conn == conn:
            client.name = username
            return

def getClientFromConn(conn):
    for client in list_of_clients:
        if client.conn == conn:
            return client

def clientthread(conn, addr): 
  
    # sends a message to the client whose user object is conn 
    conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048)
                message = message.strip()
                message = message.strip('\n')
                if message: 
                    if message.startswith("/setusername"):
                        newUser = message.split(" ")
                        print("user "+addr[0]+" renamed itself to "+newUser[1])
                        setUsername(conn, newUser[1])
                        continue

                    if message.startswith("/listchan"):
                        conn.send("channel list\n")
                        conn.send("------------\n\n")
                        for channel in list_of_channels:
                            conn.send(" * "+channel.name+"\n")
                        continue

                    if message.startswith("/createchan"):
                        newChannel = message.split(" ")
                        list_of_channels.append(Channel(newChannel[1]))
                        continue

                    if message.startswith("/joinchan"):
                        newChannel = message.split(" ")
                        client = getClientFromConn(conn)
                        client.channel = newChannel[1]
                        continue

                    """prints the message and address of the 
                    user who just sent the message on the server 
                    terminal"""
                    client = getClientFromConn(conn)
                    print ("#"+client.channel+" <" + client.name + "> " + message) 
  
                    # Calls broadcast function to send message to all 
                    message_to_send = "<" + client.name + "> " + message 
                    broadcast(message_to_send, conn, client.channel) 
  
                else: 
                    """message may have no content if the connection 
                    is broken, in this case we remove the connection"""
                    remove(conn) 
  
            except: 
                traceback.print_exc()
                #continue
  
"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection, channel): 
    for client in list_of_clients:
        if client.channel != channel:
            continue
        if client.conn!=connection: 
            try: 
                client.conn.send(message) 
            except: 
                client.conn.close() 
  
                # if the link is broken, we remove the client 
                remove(client.conn) 
  
"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept() 
  
    """Maintains a list of clients for ease of broadcasting 
    a message to all available people in the chatroom"""
    newClient = Client(conn, 'undef', 'general')
    list_of_clients.append(newClient) 
  
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
  
    # creates and individual thread for every user 
    # that connects 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close()
