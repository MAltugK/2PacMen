import pygame
from network import Network

width = 500
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

clientNumber = 0

class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height) # to draw our character
        self.vel = 3

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect) # draw our character

    def move(self): # check if we press left key, right key etc.
        keys = pygame.key.get_pressed() # dict of all pressed keys, 1: pressed, 0: released

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -=  self.vel
        
        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()
    
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height) # to redraw the x at its new position


def read_pos(str): # read a string as a tuple
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup): # write a tuple as a string
    return str(tup[0]) + "," + str(tup[1])


def redrawWinow(win, player, player2):
    win.fill((255,255,255))
    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main ():
    # run continously, constantly ask server for info
    run = True
    n = Network()
    startPos = read_pos(n.getPos()) # starting position of the client, a tuple like (50,100) as a string
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(0, 0, 100, 100, (255, 0, 0))
    print("p2 rect:", p2.rect)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(60)

        # send our current location to the server
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWinow(win, p, p2)

main()