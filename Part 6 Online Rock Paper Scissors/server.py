import socket
from _thread import *
from game import Game
import pickle

server = "10.200.115.11" # my local ip address, anyone connected to this network will be able to connect to this server
port = 5555 # usually a safe port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) # connect to a server and a port
except socket.error as e:
    str(e)

s.listen(2) # listen for connections, opens up the port
print("Server started, waiting for a connection...")

connected = set()
games = {}
idCount = 0

def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p))) # know if we are p1 pr p2

    reply = ""
    while True:
        try:
            # get, reset or move
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]  

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get": # a move
                        game.play(p, data) # send the move to the game to update it (player, move)

                    conn.sendall(pickle.dumps(game))
            else: # if game is closed
                break
        except:
            break

    print("Lost connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass

    idCount -= 1
    conn.close()


while True: # continuously look for connections
    conn, addr = s.accept() # accept connection, conn is an object addr is the IP address of the client
    print("Connected to:", addr)

    idCount += 1
    p= 0
    gameId = (idCount -1)//2 # increment gameId by 1 for each 2 players
    if idCount % 2 == 1: # create new game
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))    