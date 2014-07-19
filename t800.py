import pygame, glob, os
from random import randint
from laser import Laser
from functions import matchCentre, pointDirection, vector, pointDistance, withinViewport


class T800():
    def __init__(self, x, y, target_x, target_y, mapWidth, mapHeight):
        self.x = x
        self.y = y
        # copy the map size for this object
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        
        # use same sprite as player
        self.spriteIndex = glob.glob(os.path.join("sprites", "player", "p??.png"))
        
        # this is used for a common centre point among all sprite sub images
        self.spriteStart = pygame.image.load(self.spriteIndex[0]).convert_alpha()
        
        # this is the sprite that will be drawn for the terminator
        self.sprite = self.spriteStart
        
        # create an image for pixel collision testing
        self.hitMask = pygame.mask.from_surface(self.sprite)
        
        # sprite sub image will start at 0
        self.imageIndex = 0
        # a timer to animate the sprite
        self.imageCounter = 0
        
        # while the width and height gets larger as the sprite rotates from the centre point it's not much more
        # so close enough is good enough
        area = self.sprite.get_rect()
        self.width = area.width
        self.height = area.height
        
        # a rectangle for initial collision testing
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.attackPlayer = False
        self.destroyed = False
        
        self.direction = pointDirection(self.x, self.y, target_x, target_y)
        self.targetDirection = self.direction
        self.speed = 3
        self.armour = 4
        # a short timer before the blaster can actually fire again
        self.fireTimer = 0
    
    
    def move(self, player, lasers):
        # every second frame change the sub image of the animation 
        self.imageCounter = (self.imageCounter + 1) % 2
        
        # if the timer has been set decrement it until it hits zero
        if self.fireTimer > 0:
            self.fireTimer -= 1
        
        # Attack Player
        if self.attackPlayer and player.armour > 0:
            # point towards the player
            self.direction = pointDirection(self.x, self.y, player.x, player.y)
            # stop moving towards the player once the distance is < 100 pixels
            if pointDistance(self.x, self.y, player.x, player.y) < 100:
                self.speed = 0
            else:
                # every time the counter hits 0 
                if self.imageCounter == 0:
                    # increment the sub image index, but reset to 0 once it hits the end sub image
                    self.imageIndex = (self.imageIndex + 1) % (len(self.spriteIndex) - 1)
                self.speed = 4
        elif pointDistance(self.x, self.y, player.x, player.y) < 275 and player.armour > 0:
            # i do this second so that once the terminator starts chasing the player it will continue to do
            # so until the player is dead
            self.attackPlayer = True   
        else:
            # so either the player is dead or the terminator is not chasing
            if self.imageCounter == 0:
                self.imageIndex = (self.imageIndex + 1) % (len(self.spriteIndex) - 1)
            # continue using or set direction to the original target direction (which is straight off the map, but
            # that doesn't matter here because the player is dead or the terminator is still in the group)
            self.direction = self.targetDirection
            self.speed = 3

        
        # i'm not testing to see if the player is dead for the T800's to stop firing,
        # because i think it looks funny that they do some victory shooting
        if (self.fireTimer == 0 and pointDistance(self.x, self.y, player.x, player.y) < 275 
            and randint(0, 24) == 0):
            # once all conditions are met add a laser to the array of lasers. the colour of the laser is also
            # used for collisions with terminators or the player
            lasers.append(Laser(self.x + 25, self.y + 25, self.direction, "laserGreen.png"))
            self.fireTimer = 12
        
        # from the current direction and speed get the x, y adjustments
        (add_x, add_y) = vector(self.direction, self.speed)
        
        # move the T800
        self.x += add_x
        self.y += add_y
        
        # decide whether the terminator stays in the game, either has left the map or has been destroyed
        if self.x > self.mapWidth + 10:
            self.destroyed = True
        elif self.armour < 0:
            self.destroyed = True
            player.T800Killed += 1
        
        # load the new sprite sub image
        self.sprite = pygame.image.load(self.spriteIndex[self.imageIndex])
        # rotate the new sprite
        self.sprite = pygame.transform.rotate(self.sprite, self.direction).convert_alpha()
        
        # create a image for pixel collision testing
        self.hitMask = pygame.mask.from_surface(self.sprite)
        self.spriteCentre = matchCentre(self.spriteStart, self.sprite)
        
        # an approximate rectangle to test for collisions with lasers
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        
        
        
        
    
    def draw(self, window, viewPort):
        # check to see if any part of the terminator is within the players view port
        if (withinViewport(self.x, self.width, viewPort.x, viewPort.width) and 
                                withinViewport(self.y, self.height, viewPort.y, viewPort.height)):
            # draw the terminator, but subtract the view ports x, y position from the terminators x, y position
            # so that it will be drawn in the pygame window
            window.blit(self.sprite, (self.x + self.spriteCentre[0] - viewPort.x,
                                       self.y + self.spriteCentre[1] - viewPort.y))
            # energy bar for T800. first draw a black rectangle
            pygame.draw.rect(window, (0,0,0), (self.x - viewPort.x, self.y - viewPort.y,
                                                16, 4))
            # then draw a coloured rectangle, scaled in x, to represent the energy level
            pygame.draw.rect(window, (254,72,25), (self.x - viewPort.x, self.y - viewPort.y,
                                                4 * self.armour, 4))
        """# testing only
        pygame.draw.rect(window, (255,0,0), (self.x + self.spriteCentre[0] - viewPort.x
                                               , self.y + self.spriteCentre[1] - viewPort.y, 
                                               self.width, self.height), 1)
        """
        
        
        
        
        
        
        
