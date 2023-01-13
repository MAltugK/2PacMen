import pygame

# define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
purple = (255, 0, 255)
yellow = (255, 255, 0)


Gameicon = pygame.image.load('images/pacman.png')
pygame.display.set_icon(Gameicon)

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

    def getPos(self):
        return self.rect.left, self.rect.top

    def drawIt(self, win):
        self.draw(win)
    


    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x = x
        self.change_y = y

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

        else:
            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y

directions = {}
directions["Pinky"] = [[0, -30, 4], [15, 0, 9],[0, 15, 11],[-15, 0, 23],[0, 15, 7],[15, 0, 3],[0, -15, 3],[15, 0, 19],[0, 15, 3],[15, 0, 3],[0, 15, 3],[15, 0, 3],[0, -15, 15],[-15, 0, 7],[0, 15, 3],[-15, 0, 19],[0, -15, 11],[15, 0, 9]]
directions["Blinky"] = [[0, -15, 4],[15, 0, 9],[0, 15, 11],[15, 0, 3],[0, 15, 7],[-15, 0, 11],[0, 15, 3],[15, 0, 15],[0, -15, 15],[15, 0, 3], [0, -15, 11],[-15, 0, 3],[0, -15, 11],[-15, 0, 3],[0, -15, 3],[-15, 0, 7],[0, -15, 3],[15, 0, 15],[0, 15, 15],[-15, 0, 3],[0, 15, 3],[-15, 0, 3],[0, -15, 7],[-15, 0, 3],[0, 15, 7],[-15, 0, 11],[0, -15, 7],[15, 0, 5]]
directions["Inky"] = [[30, 0, 2],[0, -15, 4],[15, 0, 10],[0, 15, 7],[15, 0, 3],[0, -15, 3],[15, 0, 3],[0, -15, 15],[-15, 0, 15],[0, 15, 3],[15, 0, 15], [0, 15, 11],[-15, 0, 3],[0, -15, 7],[-15, 0, 11],[0, 15, 3],[-15, 0, 11],[0, 15, 7],[-15, 0, 3],[0, -15, 3],[-15, 0, 3],[0, -15, 15],[15, 0, 15],[0, 15, 3],[-15, 0, 15], [0, 15, 11],[15, 0, 3],[0, -15, 11],[15, 0, 11],[0, 15, 3],[15, 0, 1],]
directions["Clyde"] = [[-30, 0, 2],[0, -15, 4],[15, 0, 5],[0, 15, 7],[-15, 0, 11],[0, -15, 7],[-15, 0, 3], [0, 15, 7], [-15, 0, 7],[0, 15, 15],[15, 0, 15], [0, -15, 3], [-15, 0, 11], [0, -15, 7], [15, 0, 3],[0, -15, 11], [15, 0, 9],]

# Inheritime Player klassist
class Ghost(Player):
    def __init__(self, name, x, y, filename, turn, steps):
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

        self.name = name
        self.turn = turn
        self.steps = steps

    def changeLocation(self, wall_list):
        returned = self.changespeed(directions[self.name], False, self.turn, self.steps, len(directions[self.name])-1)
        self.turn = returned[0]
        self.steps = returned[1]
        self.changespeed(directions[self.name], False, self.turn,  self.steps, len(directions[self.name])-1)
        self.update(wall_list, False)


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
                elif ghost == "Clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]
    
    def drawIt(self, win):
        self.draw(win)


""" pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1 """

