import pygame, os
from functions import matchCentre, pointDistance

class Console():
    def __init__(self):
        self.spriteRadarBeam = pygame.image.load(os.path.join("sprites", "radarBeam.png")).convert_alpha()
        self.direction = 0
        # an array of tuples
        self.radarBlips = []
        # initialise at 1200. can be adjusted from 800 to 2000 in 400 increments/decrements
        self.radarRange = 1200
        # a timer to blink the energy level when it is low
        self.blinkTimer = 0
        
    
    def move(self, people, T800, player):
        # will need to add array for 'blips' on the radar
        self.direction += 10
        self.beam = pygame.transform.rotate(self.spriteRadarBeam, self.direction).convert_alpha()
        
        self.spriteCentre = matchCentre(self.spriteRadarBeam, self.beam)
        # clear radar blips
        self.radarBlips = []
        
        for f in range(len(people)):
            if pointDistance(people[f].x, people[f].y, player.x, player.y) < self.radarRange:
                self.radarBlips.append((int(750 + (people[f].x - player.x) * 47 / self.radarRange), 
                                           int(550 + (people[f].y - player.y) * 47 / self.radarRange),
                                           (0,255,0)))
        
        for f in range(len(T800)):
            if pointDistance(T800[f].x, T800[f].y, player.x, player.y) < self.radarRange:
                self.radarBlips.append((int(750 + (T800[f].x - player.x) * 47 / self.radarRange), 
                                           int(550 + (T800[f].y - player.y) * 47 / self.radarRange),
                                           (255 * (self.radarRange == 800),255 * (self.radarRange != 800),0)))
        
        
    def draw(self, window, player):
        self.blinkTimer = (self.blinkTimer + 1) % 20
        
        panelFont = pygame.font.Font(os.path.join("fonts", "keypuncn.ttf"), 20)
        
        # black rectangle panel
        pygame.draw.rect(window, (0,0,0), (0,560,800,40))
        
        scoreText = panelFont.render("Terminated:" + str(player.peopleKilled), 1, (0,200,0))
        window.blit(scoreText, (10, 570))
        scoreText = panelFont.render("T800s:" + str(player.T800Killed), 1, (0,200,0))
        window.blit(scoreText, (195, 570))
        
        # player energy rectangle
        energyText = panelFont.render("Energy:", 1, (0,200,0))
        window.blit(energyText, (345, 570))
        pygame.draw.rect(window, (0, 225, 0), (422, 570, 102, 22), True)
        pygame.draw.rect(window, (0, 225, 0), (524, 577, 4, 8), False)
        
        if player.armour > 0 and (player.armour > 3 or self.blinkTimer < 10):
            pygame.draw.rect(window, (254, 72, 25), (423, 571, 10 * player.armour, 20))
        
        radarText = panelFont.render("Range: " + str(self.radarRange), 1, (0,200,0))
        window.blit(radarText, (550, 570))
        
        # radar circles, 1 green then 1 slightly smaller black
        pygame.draw.circle(window, (0,205,0), (750,550), 50)
        pygame.draw.circle(window, (0,0,0), (750,550), 48)
        
        # draw the radar blips
        for f in range(len(self.radarBlips)):
            pygame.draw.circle(window, self.radarBlips[f][2], (self.radarBlips[f][0], self.radarBlips[f][1]), 2)
        
        # draw the radar beam
        window.blit(self.beam, (700 + self.spriteCentre[0], 500 + self.spriteCentre[1]))
        
        
