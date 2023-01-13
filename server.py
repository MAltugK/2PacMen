import socket
from _thread import *
import pickle
from game import Player, Ghost
import pygame
import game

my_address = "10.200.115.11" # my local ip address, anyone connected to this network will be able to connect to this server
my_port = 5555 # usually a safe port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((my_address, my_port))
except socket.error as e:
    str(e)

s.listen(2)
print("Server is started and is waiting for connections...")
# print("Address: ", address, "Port: ", port)



""" width = 606
height = 606
page = pygame.display.set_mode([width, height])


# keep players and ghosts on the server
players = [Player(257, 439, "images/pacman_green.png"), Player(347, 439, "images/pacman_yellow.png")]

ghosts = [Ghost("Blinky", 287, 199, "images/Blinky.png",0,0),
            Ghost("Pinky", 287, 259, "images/Pinky.png",0,0),
            Ghost("Inky", 255, 259, "images/Inky.png",0,0),
            Ghost("Clyde", 319, 259, "images/Clyde.png",0,0)]
 """
def read_pos(str): # read a string as a tuple
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup): # write a tuple as a string
    return str(tup[0]) + "," + str(tup[1])

# initial positions of players
pos = [(257, 439), (347, 439)]



def threaded_client(conn, player):
    # send their player no and the game grid (walls etc.)
    print("Client ", player , " on mission!")
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""

    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break

            else: # send the info of the other player
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
            
            conn.sendall(str.encode(make_pos(reply)))
        
        except socket.error as e:
            break
    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to ", addr, " as player", currentPlayer)
    
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1