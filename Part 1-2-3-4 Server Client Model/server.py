import socket
from _thread import *
import sys

server = "10.200.115.11" # my local ip address, anyone connected to this network will be able to connect to this server
port = 5555 # usually a safe port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) # connect to a server and a port
except socket.error as e:
    str(e)

s.listen(2) # listen for connections, opens up the port
print("Server started, waiting for a connection...")

def read_pos(str): # read a string as a tuple
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup): # write a tuple as a string
    return str(tup[0]) + "," + str(tup[1])

pos = [(0,0), (100,100)] # list of positions of our players

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data # update the information
            

            if not data:
                print("Disconnected")
                break
            else: # send the pos of other player
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", reply)
                print("Sending: ", reply)
            
            conn.sendall(str.encode(make_pos(reply))) # bak encoded yolladık

        except socket.error as e:
            break
    print("Lost connection!")
    conn.close()

currentPlayer = 0
while True: # continuously look for connections
    conn, addr = s.accept() # accept connection, conn is an object addr is the IP address of the client
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1 # keep track of the current player to update them