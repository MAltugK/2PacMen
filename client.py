import pygame
from network import Network
pygame.font.init()


width = 606
height = 606
win = pygame.display.set_mode([width, height])
pygame.display.set_caption("Pacman Client")

icon = pygame.image.load('images/pacman.png')
pygame.display.set_icon(icon)

def redrawWindow(win, player1, player2, ghost_list):
    win.fill((0, 0, 0)) # draw the maze here
    player1.draw(win)
    player2.draw(win)
    for ghost in ghost_list:
        ghost.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    p = n.getP()

    clock = pygame.time.Clock()

    # create the grid, walls

    while run:
        clock.tick(60)
        updates = n.send(p) # when you send your player info, server responds with the other player and ghosts
        p2 = updates[0]
        ghost_list = updates[1]
        for event in pygame.evet.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move() # when you move, p will be updated and will be sent at the start of the new loop turn
        
        redrawWindow(win, p, p2, ghost_list)