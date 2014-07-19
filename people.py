import pygame, glob, os
from random import randint

from functions import matchCentre, pointDirection, vector, pointDistance, withinViewport


class People():
    def __init__(self, x, y, target_x, target_y, mapWidth, mapHeight):
        self.x = x
        self.y = y
        
        self.target_x = target_x
        self.target_y = target_y
        
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        # take a randomised sprite
        fileName = "c0" + str(randint(1, 4)) + "_??.png"
        self.spriteIndex = glob.glob(os.path.join("sprites", "civ", fileName))
        
        self.spriteStart = pygame.image.load(self.spriteIndex[0]).convert_alpha()
        
        # initial sprite and sprite for pixel collision testing
        self.sprite = self.spriteStart
        self.hitMask = pygame.mask.from_surface(self.sprite)
        
        self.imageIndex = 0
        
        area = self.sprite.get_rect()
        self.width = area.width
        self.height = area.height
        # initial rectangle for collision 
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.destroyed = False
        self.direction = 0
        self.speed = 3
        # this will be set for a short duration to run in the opposite direction to where the player is once seen
        self.runAwayTimer = 0
    
    
    def move(self, player):
        # update index for sprite animation
        self.imageIndex = (self.imageIndex + 1) % 20
        
        # decrement the run away timer if it has been set
        if self.runAwayTimer > 0:
            self.runAwayTimer -= 1
        
        # run away, run away
        distance = pointDistance(self.x, self.y, player.x, player.y)
        if (distance < 175):
            # if the player is too close keep adjusting the run away direction
            self.direction = pointDirection(self.x, self.y, player.x, player.y) + 180
        elif (distance < 275 and self.runAwayTimer == 0):
            # set a new direction to run away from the player
            self.direction = pointDirection(self.x, self.y, player.x, player.y) + 180
            # set a random time to run in this direction
            self.runAwayTimer = randint(80, 130)
        elif self.runAwayTimer == 0:
            # set direction to the original target location off the map somewhere to the right
            self.direction = pointDirection(self.x, self.y, self.target_x, self.target_y)
        
        # get the x and y adjustments from the current speed and direction
        (add_x, add_y) = vector(self.direction, self.speed)
        
        # move the person
        self.x += add_x
        self.y += add_y
        
        # off the map - escaped!
        if self.x > self.mapWidth + 10:
            self.destroyed = True
        
        # update the sprite
        self.sprite = pygame.image.load(self.spriteIndex[self.imageIndex])
        self.sprite = pygame.transform.rotate(self.sprite, self.direction).convert_alpha()
        
        # update the pixel sprite for collision testing
        self.hitMask = pygame.mask.from_surface(self.sprite)
        self.spriteCentre = matchCentre(self.spriteStart, self.sprite)
        self.width = self.spriteCentre[2]
        self.height = self.spriteCentre[3]
        # update the rectangle for initial collision testing
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        
    
    def draw(self, window, viewPort):
        # if any pixel of the sprite is within the view port then draw the sprite
        if (withinViewport(self.x, self.width, viewPort.x, viewPort.width) and 
                                withinViewport(self.y, self.height, viewPort.y, viewPort.height)):
            # not forgetting to subtract the view port x, y position from the objects x, y position so that the
            # person appears inside the pygame window
            window.blit(self.sprite, (self.x + self.spriteCentre[0] - viewPort.x,
                                       self.y + self.spriteCentre[1] - viewPort.y))
        """# testing only
        pygame.draw.rect(window, (255,0,0), (self.x + self.spriteCentre[0] - viewPort.x
                                               , self.y + self.spriteCentre[1] - viewPort.y, 
                                               self.width, self.height), 1)
        """
        
        
        
        
        
        
        
