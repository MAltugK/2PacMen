import pygame

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