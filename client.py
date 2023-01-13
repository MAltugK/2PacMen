import pygame
from network import Network
pygame.font.init()
import game
import pickle
from game import Player, Ghost, Block
import time

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)

width = 606
height = 606
win = pygame.display.set_mode([width, height])
pygame.display.set_caption("Pacman Client")

icon = pygame.image.load('images/pacman.png')
pygame.display.set_icon(icon)

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

clientNumber = 0

def read_pos(str): # read a string as a tuple
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup): # write a tuple as a string
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win, all_sprites_list):
    all_sprites_list.draw(win)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    
    p = Player(startPos[0], startPos[1], "images/pacman_green.png")
    p2 = Player(347, 439,"images/pacman_yellow.png")
    # necessary lists
    all_sprites_list = pygame.sprite.RenderPlain()
    all_sprites_list.add(p)
    all_sprites_list.add(p2)
    

    # create the grid, walls
    wall_list = game.setupRoomOne(all_sprites_list)
    gate = game.setupGate(all_sprites_list)
    block_list = pygame.sprite.RenderPlain()
    monsta_list = pygame.sprite.RenderPlain()
    pacman_collide = pygame.sprite.RenderPlain()
    ghost_list = [Ghost("Blinky", 287, 199, "images/Blinky.png",0,0),
            Ghost("Pinky", 287, 259, "images/Pinky.png",0,0),
            Ghost("Inky", 255, 259, "images/Inky.png",0,0),
            Ghost("Clyde", 319, 259, "images/Clyde.png",0,0)]
    for ghost in ghost_list:
        all_sprites_list.add(ghost)
        monsta_list.add(ghost)

    # draw blocks
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block((255, 255, 0), 4, 4)

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

    # draw them
    wall_list.draw(win)
    gate.draw(win)
    all_sprites_list.draw(win)

    clock = pygame.time.Clock()

    bll = len(block_list)

    yellow_score = 0
    green_score = 0
    done = False

    i = 0
    time.sleep(5)

    while done == False:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.rect.left, p.rect.y))))
        p2.rect.left = p2Pos[0]
        p2.rect.top = p2Pos[1]

        # update the other pacman
        p2.update(wall_list, gate)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
            #print("event type and key: ", event.type, event.key)
                if event.type == pygame.QUIT:
                    done = True
                send_msg = ""
            # make and send your move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    p.changespeed(-30, 0)
                    print("a down")
                    #s.send('a'.encode("utf-8"))
                    send_msg = "a"
                if event.key == pygame.K_d:
                    p.changespeed(30, 0)
                    print("d down")
                    #s.send('d'.encode("utf-8"))
                    send_msg = "d"
                if event.key == pygame.K_w:
                    p.changespeed(0, -30)
                    #s.send('w'.encode("utf-8"))
                    print("w down")
                    send_msg = "w"
                if event.key == pygame.K_s:
                    p.changespeed(0, 30)
                    #s.send('s'.encode("utf-8"))
                    send_msg = "s"
                    print("s down")
                #conn.send(send_msg.encode('utf-8'))

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        p.changespeed(30, 0)
                        #s.send('d'.encode("utf-8"))
                        send_msg = "a"
                        print("a up")
                    if event.key == pygame.K_d:
                        p.changespeed(-30, 0)
                        #s.send('a'.encode("utf-8"))
                        send_msg = "d"
                        print("d up")
                    if event.key == pygame.K_w:
                        p.changespeed(0, 30)
                        #s.send('s'.encode("utf-8"))
                        send_msg = "w"
                        print("w up")
                    if event.key == pygame.K_s:
                        p.changespeed(0, -30)
                        #s.send('w'.encode("utf-8"))
                        print("s up")
                    #conn.send(send_msg.encode('utf-8'))
                    print("p was...", p.getPos(), type(p.getPos))
                #n.send(make_pos((p.rect.left, p.rect.top)))
                p.update(wall_list, gate)
            
            # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT        
        
            
            p2.update(wall_list, gate)
        
        redrawWindow(win, all_sprites_list)
        
        blocks_hit_list_yellow = pygame.sprite.spritecollide(p, block_list, True)
        blocks_hit_list_green = pygame.sprite.spritecollide(p2, block_list, True)

        # Check the list of collisions.
        if len(blocks_hit_list_yellow) > 0:
            green_score += len(blocks_hit_list_yellow)
        if len(blocks_hit_list_green) > 0:
            yellow_score += len(blocks_hit_list_green)
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        win.fill((0, 0, 0))

        wall_list.draw(win)
        gate.draw(win)
        all_sprites_list.draw(win)
        monsta_list.draw(win)

        text = font.render("Green Score: " + str(green_score) + "/" + str(bll), True, red)
        win.blit(text, [10, 10])
        text = font.render("Yellow Score: " + str(yellow_score) + "/" + str(bll), True, red)
        win.blit(text, [10, 30])

        if yellow_score + green_score == bll:
            if yellow_score > green_score:
                doNext("Congratulations, Yellow won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                       wall_list, gate, win, font, clock)
            if green_score > yellow_score:
                doNext("Congratulations, Green won!", 145, all_sprites_list, block_list, monsta_list, pacman_collide,
                       wall_list, gate, win, font, clock)
        monsta_hit_list_yellow = pygame.sprite.spritecollide(p, monsta_list, False)
        monsta_hit_list_green = pygame.sprite.spritecollide(p2, monsta_list, False)

        if monsta_hit_list_yellow:
            doNext("Game Over, Yellow Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list,
                   gate, win, font, clock)
        if monsta_hit_list_green:
            doNext("Game Over, Green Wins", 180, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list,
                   gate, win, font, clock)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        pygame.display.flip()

        clock.tick(10)
    
    def doNext(message, left, all_sprites_list, block_list, monsta_list, pacman_collide, wall_list, gate, screen, font, clock):
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
                        

            # Grey background
            w = pygame.Surface((400, 200))  # the size of your rect
            w.set_alpha(10)  # alpha level
            w.fill((128, 128, 128))  # this fills the entire surface
            screen.blit(w, (100, 200))  # (0,0) are the top-left coordinates

            # Won or lost
            text1 = font.render(message, True, (255, 255, 255))
            screen.blit(text1, [left, 233])

            text2 = font.render("To play again, press ENTER.", True, (255, 255, 255))
            screen.blit(text2, [135, 303])
            text3 = font.render("To quit, press ESCAPE.", True, (255, 255, 255))
            screen.blit(text3, [165, 333])

            pygame.display.flip()

            clock.tick(10)

main()