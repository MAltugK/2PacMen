import os
import socket
import ssl
import time
from _thread import *

import pygame
from pyngrok import ngrok, conf, installer

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)
hostOrClient = ""
Gameicon = pygame.image.load('images/pacman.png')
pygame.display.set_icon(Gameicon)

""" root = Tk()
IPpopup = Tk()
Label(IPpopup, text='IP Address').grid(row=0)
Label(IPpopup, text='Port').grid(row=1)
IpAddressBox = Text(IPpopup, height=10, width=25)
PortBox = Text(IPpopup, height=10, width=25)
IpAddressBox.grid(row=0, column=1)
PortBox.grid(row=1, column=1) """


# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()

    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # return our new list
    return wall_list


def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate


# This class represents the ball
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    # This class represents the bar at the bottom that the player controls


class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):
        # Get the old position, in case we need to go back to it

        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        prev_y = old_y + self.prev_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


# Inheritime Player klassist
class Ghost(Player):
    # Change the speed of the ghost
    def changespeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


Pinky_directions = [
    [0, -30, 4],
    [15, 0, 9],
    [0, 15, 11],
    [-15, 0, 23],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 19],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 7],
    [0, 15, 3],
    [-15, 0, 19],
    [0, -15, 11],
    [15, 0, 9]
]

Blinky_directions = [
    [0, -15, 4],
    [15, 0, 9],
    [0, 15, 11],
    [15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [15, 0, 15],
    [0, -15, 15],
    [15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 7],
    [0, -15, 3],
    [15, 0, 15],
    [0, 15, 15],
    [-15, 0, 3],
    [0, 15, 3],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 5]
]

Inky_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 10],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 15],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [-15, 0, 11],
    [0, 15, 7],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 3],
    [0, -15, 15],
    [15, 0, 15],
    [0, 15, 3],
    [-15, 0, 15],
    [0, 15, 11],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 11],
    [0, 15, 3],
    [15, 0, 1],
]

Clyde_directions = [
    [-30, 0, 2],
    [0, -15, 4],
    [15, 0, 5],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 7],
    [0, 15, 15],
    [15, 0, 15],
    [0, -15, 3],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 9],
]

pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1


def host_new_server_action():
    # an un-reserved port number
    port = 50000
    """ root.destroy()
    IPpopup.destroy() """
    # configure ngrok
    pyngrok_config = conf.get_default()
    if not os.path.exists(pyngrok_config.ngrok_path):
        myssl = ssl.create_default_context()
        myssl.check_hostname = False
        myssl.verify_mode = ssl.CERT_NONE
        installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)
    # open a tcp tunnel, get its IP and port to give to the client
    tunnel_url = ngrok.connect(port, proto='tcp').public_url
    host = socket.gethostbyname(tunnel_url.strip('tcp://').split(':')[0])
    port = int(tunnel_url.strip('tcp://').split(':')[1])
    print("To join, the other player must enter this code: ", host, ":", port)
    # create the socket and bind it to local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 50000))
    s.listen(1)

    conn, addr = s.accept()
    print("Connected from ", addr)
    start_game_host(conn)



def connect_session(ip, port):
    """ IpAddress = IpAddressBox.get("1.0", "end-1c")
    Port = PortBox.get("1.0", "end-1c")
    IPpopup.destroy()
    print(IpAddress)
    print(Port) """
    print("I will connect to ", ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((str(ip), int(port)))
        print("Connected!")

    except socket.error as er_msg:
        print("Error while connecting:", er_msg)

    start_game_client(s)



""" def host_action():
    # root.destroy()
    print("host action")
    host_new_server_action()
    hostOrClient = "Host"
    print("pout of host action")
    mainloop()


def client_action():
    root.destroy()
    hostOrClient = "Client"
    connectButton = Button(IPpopup, text="Connect Session", command=connect_session).grid(row=2)
    mainloop()
 """


def start_game_host(conn):
    # Call this function so the Pygame library can initialize itself
    pygame.init()

    # Create an 606x606 sized screen
    screen = pygame.display.set_mode([606, 606])

    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'RenderPlain.'

    # Set the title of the window
    pygame.display.set_caption('Pacman Server')

    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())

    # Used for converting color maps and such
    background = background.convert()

    # Fill the screen with a black background
    background.fill(black)

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)

    # default locations for Pacman and monstas
    w = 303 - 16  # Width
    p_h = (7 * 60) + 19  # Pacman height
    m_h = (4 * 60) + 19  # Monster height
    b_h = (3 * 60) + 19  # Binky height
    i_w = 303 - 16 - 32  # Inky width
    c_w = 303 + (32 - 16)  # Clyde width

    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monsta_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    # Create the player paddle object
    Pacman1 = Player(w - 30, p_h, "images/pacman_green.png")  # host
    Pacman2 = Player(w + 30, p_h, "images/pacman_yellow.png")  # client

    all_sprites_list.add(Pacman1)
    pacman_collide.add(Pacman1)
    all_sprites_list.add(Pacman2)
    pacman_collide.add(Pacman2)

    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)

    Clyde = Ghost(c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)

                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)

    bll = len(block_list)

    yellow_score = 0
    green_score = 0
    done = False

    time.sleep(1)

    while done == False:

        # receive client's move
        messageclient = ""

        def recv_data():
            messageclient = conn.recv(1024).decode("utf-8")
            print("Host received: ", messageclient)
            for letter in messageclient:
                if letter == 'a':
                    Pacman2.changespeed(-30, 0)
                if letter == 'd':
                    Pacman2.changespeed(30, 0)
                if letter == 'w':
                    Pacman2.changespeed(0, -30)
                if letter == 's':
                    Pacman2.changespeed(0, 30)

        start_new_thread(recv_data, ())





        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            # print("event type and key: ", event.type, event.key)
            if event.type == pygame.QUIT:
                done = True

            send_msg = ""
            # make and send your move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    Pacman1.changespeed(-30, 0)
                    # s.send('a'.encode("utf-8"))
                    send_msg = "h"
                if event.key == pygame.K_k:
                    Pacman1.changespeed(30, 0)
                    # s.send('d'.encode("utf-8"))
                    send_msg = "k"
                if event.key == pygame.K_u:
                    Pacman1.changespeed(0, -30)
                    # s.send('w'.encode("utf-8"))
                    send_msg = "u"
                if event.key == pygame.K_j:
                    Pacman1.changespeed(0, 30)
                    # s.send('s'.encode("utf-8"))
                    send_msg = "j"

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_h:
                    Pacman1.changespeed(30, 0)
                    send_msg = "k"
                if event.key == pygame.K_k:
                    Pacman1.changespeed(-30, 0)
                    send_msg = "h"
                if event.key == pygame.K_u:
                    Pacman1.changespeed(0, 30)
                    send_msg = "j"
                if event.key == pygame.K_j:
                    Pacman1.changespeed(0, -30)
                    send_msg = "u"

            if send_msg != "":
                print("host at line 620 with message ", send_msg)
                conn.send(send_msg.encode('utf-8'))
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT

        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Pacman1.update(wall_list, gate)
        Pacman2.update(wall_list, gate)

        # returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        # p_turn = returned[0]
        # p_steps = returned[1]
        # Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        # Pinky.update(wall_list, False)
        #
        returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)
        #
        # returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        # i_turn = returned[0]
        # i_steps = returned[1]
        # Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        # Inky.update(wall_list, False)
        #
        # returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        # c_turn = returned[0]
        # c_steps = returned[1]
        # Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        # Clyde.update(wall_list, False)

        # See if the Pacman block has collided with anything.
        blocks_hit_list_yellow = pygame.sprite.spritecollide(Pacman1, block_list, True)
        blocks_hit_list_green = pygame.sprite.spritecollide(Pacman2, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list_yellow) > 0:
            green_score += len(blocks_hit_list_yellow)
        if len(blocks_hit_list_green) > 0:
            yellow_score += len(blocks_hit_list_green)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)

        text = font.render("Green Score: " + str(green_score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 10])
        text = font.render("Yellow Score: " + str(yellow_score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 30])

        if yellow_score + green_score == bll:
            if yellow_score > green_score:
                doNext_h("Congratulations, Yellow won!", 145, all_sprites_list, block_list, monsta_list,
                         pacman_collide,
                         wall_list, gate, screen, font, clock)
            if green_score > yellow_score:
                doNext_h("Congratulations, Green won!", 145, all_sprites_list, block_list, monsta_list,
                         pacman_collide,
                         wall_list, gate, screen, font, clock)
        monsta_hit_list_yellow = pygame.sprite.spritecollide(Pacman1, monsta_list, False)
        monsta_hit_list_green = pygame.sprite.spritecollide(Pacman2, monsta_list, False)

        if monsta_hit_list_yellow:
            doNext_h("Game Over, Yellow Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide,
                     wall_list,
                     gate, screen, font, clock)
        if monsta_hit_list_green:
            doNext_h("Game Over, Green Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide,
                     wall_list,
                     gate, screen, font, clock)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def start_game_client(s):
    """ root.title("Popup")
    host_button = Button(root, text="Host", command=host_action)
    client_button = Button(root, text="Client", command=client_action)
    root.geometry('100x50')
    host_button.pack(side='left')
    client_button.pack(side='right')
    print("host at 445")
    root.mainloop()
    print("host at 446") """
    # Call this function so the Pygame library can initialize itself
    pygame.init()
    # Create an 606x606 sized screen
    screen = pygame.display.set_mode([606, 606])
    # This is a list of 'sprites.' Each block in the program is
    # added to this list. The list is managed by a class called 'RenderPlain.'

    # Set the title of the window
    pygame.display.set_caption('Pacman Client')
    # Create a surface we can draw on
    background = pygame.Surface(screen.get_size())
    # Used for converting color maps and such
    background = background.convert()
    # Fill the screen with a black background
    background.fill(black)
    clock = pygame.time.Clock()
    pygame.font.init()
    font = pygame.font.Font("freesansbold.ttf", 24)
    # default locations for Pacman and monstas
    w = 303 - 16  # Width
    p_h = (7 * 60) + 19  # Pacman height
    m_h = (4 * 60) + 19  # Monster height
    b_h = (3 * 60) + 19  # Binky height
    i_w = 303 - 16 - 32  # Inky width
    c_w = 303 + (32 - 16)  # Clyde width
    all_sprites_list = pygame.sprite.RenderPlain()
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()
    wall_list = setupRoomOne(all_sprites_list)
    gate = setupGate(all_sprites_list)
    p_turn = 0
    p_steps = 0
    b_turn = 0
    b_steps = 0
    i_turn = 0
    i_steps = 0
    c_turn = 0
    c_steps = 0
    # Create the player paddle object
    Pacman1 = Player(w - 30, p_h, "images/pacman_green.png")  # host
    Pacman2 = Player(w + 30, p_h, "images/pacman_yellow.png")  # client
    all_sprites_list.add(Pacman1)
    pacman_collide.add(Pacman1)
    all_sprites_list.add(Pacman2)
    pacman_collide.add(Pacman2)
    Blinky = Ghost(w, b_h, "images/Blinky.png")
    monsta_list.add(Blinky)
    all_sprites_list.add(Blinky)
    Pinky = Ghost(w, m_h, "images/Pinky.png")
    monsta_list.add(Pinky)
    all_sprites_list.add(Pinky)
    Inky = Ghost(i_w, m_h, "images/Inky.png")
    monsta_list.add(Inky)
    all_sprites_list.add(Inky)
    Clyde = Ghost(c_w, m_h, "images/Clyde.png")
    monsta_list.add(Clyde)
    all_sprites_list.add(Clyde)
    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(yellow, 4, 4)
                # Set a random location for the block
                block.rect.x = (30 * column + 6) + 26
                block.rect.y = (30 * row + 6) + 26
                b_collide = pygame.sprite.spritecollide(block, wall_list, False)
                p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the block to the list of objects
                    block_list.add(block)
                    all_sprites_list.add(block)
    bll = len(block_list)
    yellow_score = 0
    green_score = 0
    done = False
    i = 0
    time.sleep(1)
    message = ''
    """ if hostOrClient == "Host":
        s.accept() """
    while done == False:

        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():

            # print("event type and key: ", event.type, event.key)

            if event.type == pygame.QUIT:
                done = True

            send_msg = ""
            # send your move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Pacman2.changespeed(-30, 0)
                    # s.send('a'.encode("utf-8"))
                    send_msg = "a"
                if event.key == pygame.K_d:
                    Pacman2.changespeed(30, 0)
                    # s.send('d'.encode("utf-8"))
                    send_msg = "d"
                if event.key == pygame.K_w:
                    Pacman2.changespeed(0, -30)
                    # s.send('w'.encode("utf-8"))
                    send_msg = "w"
                if event.key == pygame.K_s:
                    Pacman2.changespeed(0, 30)
                    # s.send('s'.encode("utf-8"))
                    send_msg = "s"
                # s.send(send_msg.encode('utf-8'))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    Pacman2.changespeed(30, 0)
                    # s.send('d'.encode("utf-8"))
                    send_msg = "d"
                if event.key == pygame.K_d:
                    Pacman2.changespeed(-30, 0)
                    # s.send('a'.encode("utf-8"))
                    send_msg = "a"
                if event.key == pygame.K_w:
                    Pacman2.changespeed(0, 30)
                    # s.send('s'.encode("utf-8"))
                    send_msg = "s"
                if event.key == pygame.K_s:
                    Pacman2.changespeed(0, -30)
                    # s.send('w'.encode("utf-8"))
                    send_msg = "w"
                # s.send(send_msg.encode('utf-8'))
            if send_msg != "":
                s.send(send_msg.encode('utf-8'))
                print("client at line 855 sent ", send_msg)

        messagehost = ""

        def recv_data():
            messagehost = s.recv(1024).decode('utf8')
            print("Received ", messagehost)
            for letter in messagehost:
                if letter == 'h':
                    Pacman1.changespeed(-30, 0)
                if letter == 'k':
                    Pacman1.changespeed(30, 0)
                if letter == 'u':
                    Pacman1.changespeed(0, -30)
                if letter == 'j':
                    Pacman1.changespeed(0, 30)

        messagehost = start_new_thread(recv_data, ())

            # update the host pacman


        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        Pacman1.update(wall_list, gate)
        Pacman2.update(wall_list, gate)
        # returned = Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        # p_turn = returned[0]
        # p_steps = returned[1]
        # Pinky.changespeed(Pinky_directions, False, p_turn, p_steps, pl)
        # Pinky.update(wall_list, False)
        #
        returned = Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changespeed(Blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)
        #
        # returned = Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        # i_turn = returned[0]
        # i_steps = returned[1]
        # Inky.changespeed(Inky_directions, False, i_turn, i_steps, il)
        # Inky.update(wall_list, False)
        #
        # returned = Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        # c_turn = returned[0]
        # c_steps = returned[1]
        # Clyde.changespeed(Clyde_directions, "clyde", c_turn, c_steps, cl)
        # Clyde.update(wall_list, False)
        # See if the Pacman block has collided with anything.
        blocks_hit_list_yellow = pygame.sprite.spritecollide(Pacman1, block_list, True)
        blocks_hit_list_green = pygame.sprite.spritecollide(Pacman2, block_list, True)
        # Check the list of collisions.
        if len(blocks_hit_list_yellow) > 0:
            green_score += len(blocks_hit_list_yellow)
        if len(blocks_hit_list_green) > 0:
            yellow_score += len(blocks_hit_list_green)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monsta_list.draw(screen)
        text = font.render("Green Score: " + str(green_score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 10])
        text = font.render("Yellow Score: " + str(yellow_score) + "/" + str(bll), True, red)
        screen.blit(text, [10, 30])
        if yellow_score + green_score == bll:
            if yellow_score > green_score:
                doNext_c("Congratulations, Yellow won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                         wall_list, gate, screen, font, clock)
            if green_score > yellow_score:
                doNext_c("Congratulations, Green won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                         wall_list, gate, screen, font, clock)
        monsta_hit_list_yellow = pygame.sprite.spritecollide(Pacman1, monsta_list, False)
        monsta_hit_list_green = pygame.sprite.spritecollide(Pacman2, monsta_list, False)

        if monsta_hit_list_yellow:
            doNext_c("Game Over, Yellow Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide,
                     wall_list,
                     gate, screen, font, clock)
        if monsta_hit_list_green:
            doNext_c("Game Over, Green Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list,
                     gate, screen, font, clock)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)


def doNext_h(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate, screen, font,
             clock):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    start_game_host()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


def doNext_c(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate, screen, font,
             clock):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del block_list
                    del monsta_list
                    del pacman_collide
                    del wall_list
                    del gate
                    start_game_client()

        # Grey background
        w = pygame.Surface((400, 200))  # the size of your rect
        w.set_alpha(10)  # alpha level
        w.fill((128, 128, 128))  # this fills the entire surface
        screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

        # Won or lost
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, white)
        screen.blit(text2, [135, 303])
        text3 = font.render("To quit, press ESCAPE.", True, white)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


if __name__ == "__main__":

    print("Welcome, please write 1 for starting a game, or 0 for joining a game.")

    start_or_join = int(input())

    if start_or_join == 1:
        print("server")
        host_new_server_action()

    elif start_or_join == 0:
        print("client")
        print("Please enter the ip of the game...")
        ip = input()
        print("Please enter the port of the game...")
        port = input()
        connect_session(ip, port)
    else:
        print("You must write 0 for joining a game or 1 for hosting a game. Please run the program again.")

    print("main ended")

# startGame()

# pygame.quit()
