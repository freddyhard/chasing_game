import pygame, glob, os

from laser import Laser
from functions import matchCentre, limits, pointDirection, vector

class T1000():
    def __init__(self, x, y, mapWidth, mapHeight):
        self.x = x
        self.y = y
        
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight

        self.spriteIndex = glob.glob(os.path.join("sprites", "player", "p??.png"))
        # start in a standing position
        self.spriteStart = pygame.image.load(self.spriteIndex[len(self.spriteIndex) - 1]).convert_alpha()
        
        self.sprite = self.spriteStart
        self.hitMask = pygame.mask.from_surface(self.sprite)
        
        self.imageIndex = 0
        self.imageCounter = 0
        
        area = self.sprite.get_rect()
        self.width = area.width
        self.height = area.height
        
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.direction = 0
        self.speed = 5
        self.armour = 10
        
        self.radarRange = 1200
        
        self.peopleKilled = 0
        self.T800Killed = 0
        
        self.fireTimer = 0
    
    
    def reinit(self):
        # a new game is being started so reset all these values
        self.peopleKilled = 0
        self.T800Killed = 0
        self.armour = 10
        self.radarRange = 1200
        self.x = 3500
        self.y = 2000
        
    
    
    def move(self, viewPort, lasers):
        # assume the player is not pressing any keys
        add_x = 0
        add_y = 0
        strafe_x = 0
        strafe_y = 0
        running = False
        
        # every other frame update the player's sprite for animation
        self.imageCounter = (self.imageCounter + 1) % 2
        
        if self.fireTimer > 0:
            self.fireTimer -= 1
        
        # stops the player's energy bar been drawn with a negative value!
        if self.armour < 0:
            self.armour = 0
        
        # get the mouse position
        mouse_xy = pygame.mouse.get_pos()
        
        # see if left mouse button is pressed. we are not doing anything with middle or right mouse buttons
        (fire, button2, button3) = pygame.mouse.get_pressed()
        
        # only if the player is alive
        if self.armour > 0:
            # set the player's direction to look at the mouse position. keep in mind the player's position needs to
            # be in relation to the view port where the mouse can only be within
            self.direction = pointDirection(self.x + self.width / 2 - viewPort.x, self.y + self.height / 2 - viewPort.y
                                        , mouse_xy[0], mouse_xy[1])
            
            # get the keys currently being pressed
            userInput = pygame.key.get_pressed()
            
            # player movement. forward is preferred to backwards; hence the elif
            if userInput[pygame.K_UP]:
                # get values to move player if up key is pressed
                (add_x, add_y) = vector(self.direction, self.speed)
                running = True
            elif userInput[pygame.K_DOWN]:
                # get values to move player if down key is pressed
                (add_x, add_y) = vector(self.direction, -self.speed * 0.5)
                running = True
            
            # only side step if not running forwards/backwards
            if not running:
                # stop player animation, by using the last sub image of the array
                self.imageIndex = len(self.spriteIndex) - 1
                self.sprite = self.spriteStart
                
                # check if the player wants to side step left/right. this time the player can press left and right
                # at the same time and both will nullify each other
                if userInput[pygame.K_LEFT]:
                    strafe = vector(self.direction + 90, self.speed * 0.7)
                    strafe_x += strafe[0]
                    strafe_y += strafe[1]
                if userInput[pygame.K_RIGHT]:
                    strafe = vector(self.direction - 90, self.speed * 0.7)
                    strafe_x += strafe[0]
                    strafe_y += strafe[1]
            # the player is moving, so update the sprite index for animation
            elif self.imageCounter == 0:
                # -2 because the last frame is a standing image, so we skip that one
                self.imageIndex = (self.imageIndex + 1) % (len(self.spriteIndex) - 2)
            # let the player fire if conditions are met
            if fire and self.fireTimer == 0:
                # set this timer to delay the auto firing. 0.3 seconds because fps = 40
                self.fireTimer = 12
                # add the laser to the array of lasers
                lasers.append(Laser(self.x + 25, self.y + 25, self.direction, "laserRed.png"))
            
            # move the player
            self.x += add_x + strafe_x
            self.y += add_y + strafe_y
            
            # stop player from moving off the map
            self.x = limits(self.x, 0, self.mapWidth, self.width)
            self.y = limits(self.y, 0, self.mapHeight, self.height)
        
        # update the players sprite
        self.sprite = pygame.image.load(self.spriteIndex[self.imageIndex])
        self.sprite = pygame.transform.rotate(self.sprite, self.direction).convert_alpha()
        
        # update the sprite for a pixel collision test
        self.hitMask = pygame.mask.from_surface(self.sprite)
        self.spriteCentre = matchCentre(self.spriteStart, self.sprite)
        self.width = self.spriteCentre[2]
        self.height = self.spriteCentre[3]
        # update the rectangle for initial collision test
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)        
        
        
    
    def draw(self, window, viewPort):
        # the player has to be within the view port, so just draw the player if this function is called
        window.blit(self.sprite, (self.x + self.spriteCentre[0] - viewPort.x,
                                   self.y + self.spriteCentre[1] - viewPort.y))
        """
        # testing only
        pygame.draw.rect(window, (255,0,0), (self.x + self.spriteCentre[0] - viewPort.x
                                               , self.y + self.spriteCentre[1] - viewPort.y, 
                                               self.width, self.height), 1)
        """
        
        
        
        
        
        
        
