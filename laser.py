import pygame, math, os
from functions import matchCentre


class Laser():
    def __init__(self, creator_x, creator_y, directionDEGREE, spriteLaser):
        
        spriteStart = pygame.image.load(os.path.join("sprites", spriteLaser)).convert_alpha()
        
        # use a solid image for the mask. the laser sprite is too small with too much
        # transparency for good collision testing
        maskSprite = os.path.join("sprites", "laserMask.png")
        
        maskStart = pygame.transform.rotate(pygame.image.load(maskSprite), 
                                            directionDEGREE).convert_alpha()
        
        self.hitMask = pygame.mask.from_surface(maskStart)
        self.sprite = pygame.transform.rotate(spriteStart, directionDEGREE).convert_alpha()
        
        area = self.sprite.get_rect()
        self.width = area[2]
        self.height = area[3]
        
        # convert to radians 
        directionRADIAN = math.radians(directionDEGREE)
        # from the centre of the sprite it is -0.548549402 radians with magnitude 20.095
        # is the precise position to launch laser from the blaster
        # i placed the laser sprite over the player sprite and measured the pixels in photoshop
        self.x = creator_x + math.cos(directionRADIAN - 0.548549402) * 20.095 - self.width / 2
        self.y = creator_y - math.sin(directionRADIAN - 0.548549402) * 20.095 - self.height / 2
        
        
        # initial collision rectangle
        self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        self.destroyed = False
        
        # since the lasers move at a set speed and direction the x, y offset only needs to be calculated once
        self.add_x = math.cos(directionRADIAN) * 18
        self.add_y = -math.sin(directionRADIAN) * 18
        
        # the length of time the laser will exist for
        self.lifeTimer = 28
        
        # see who fired by colour, so they cannot hit themselves as laser is created
        if spriteLaser == "laserRed.png":
            self.hitPlayer = False
            self.hitT800s = True
            # stolen from star wars game, back in the 90's
            soundLaser = pygame.mixer.Sound(os.path.join("sounds", "pistol.wav"))
        else:
            self.hitPlayer = True
            self.hitT800s = False
            # stolen from star wars game, back in the 90's
            soundLaser = pygame.mixer.Sound(os.path.join("sounds", "blaster.wav"))
        
        
        soundLaser.set_volume(0.5)
        soundLaser.play()
        # no idea where i got these sounds. these are used when the laser hits a terminator or a person
        self.laserHit = pygame.mixer.Sound(os.path.join("sounds", "hit.wav"))
        self.bodyhit = pygame.mixer.Sound(os.path.join("sounds", "hit2.wav"))

    

    def move(self, player, people, T800s):
        
        if self.lifeTimer > 0 and self.lifeTimer < 28:
            # the and < 28 means that it will not move the laser in the first frame.
            # this draws the laser from the blaster. i was just being pernickety
            self.x += self.add_x
            self.y += self.add_y
            self.spriteArea = pygame.Rect(self.x, self.y, self.width, self.height)
        elif self.lifeTimer == 0:
            self.destroyed = True
        
        # decrement the laser active timer
        self.lifeTimer -= 1
        
        # test for collision with people. a laser from the terminator or the player will destroy a person
        if not self.destroyed:
            for f in range(len(people)):
                # quick test with rectangle first
                if self.spriteArea.colliderect(people[f].spriteArea):
                    # precise test using pixels
                    x_offset = self.spriteArea[0] - people[f].spriteArea[0]
                    y_offset = self.spriteArea[1] - people[f].spriteArea[1]
                    if people[f].hitMask.overlap(self.hitMask, (x_offset, y_offset)):
                        # set this laser as destroyed so it will not collide again
                        self.destroyed = True
                        self.bodyhit.play()
                        # set the person it hit as destroyed
                        people[f].destroyed = True
                        # increase the players score
                        player.peopleKilled += 1
                        # exit this loop
                        break
        
        # if laser is active and has been fired by the player
        if not self.destroyed and self.hitT800s:
            for f in range(len(T800s)):
                # quick test with rectangle first
                if self.spriteArea.colliderect(T800s[f].spriteArea):
                    # precise test using pixels
                    x_offset = self.spriteArea[0] - T800s[f].spriteArea[0]
                    y_offset = self.spriteArea[1] - T800s[f].spriteArea[1]
                    if T800s[f].hitMask.overlap(self.hitMask, (x_offset, y_offset)):
                        self.destroyed = True
                        self.laserHit.play()
                        T800s[f].armour -= 1
                        T800s[f].attackPlayer = True
                        break
        
        # if laser is active and has been fired by a terminator
        if not self.destroyed and self.hitPlayer:
            if self.spriteArea.colliderect(player.spriteArea):
                x_offset = self.spriteArea[0] - player.spriteArea[0]
                y_offset = self.spriteArea[1] - player.spriteArea[1]
                if player.hitMask.overlap(self.hitMask, (x_offset, y_offset)):
                    self.destroyed = True
                    self.laserHit.play()
                    player.armour -= 1
        
        
                

    def draw(self, window, viewPort):
        # not doing a test to see if within view of viewport - because none can
        # be created outside of the view port 
        window.blit(self.sprite, (self.x - viewPort.x, self.y - viewPort.y))
        
        #pygame.draw.rect(window, (0,255,0), (self.x - viewPort.x, self.y - viewPort.y, self.width, self.height), 1)
        
    
    
