import pygame
from functions import withinViewport

class MapSection():
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        
        self.sprite = pygame.image.load(sprite)
        
        area = self.sprite.get_rect()
        self.width = area.width
        self.height = area.height
    
    
    def draw(self, window, viewPort):
        # test to see if any part of the sprite is visible within the view port
        if (withinViewport(self.x, self.width, viewPort.x, viewPort.width) and 
                                withinViewport(self.y, self.height, viewPort.y, viewPort.height)):
            # if so then draw this map
            window.blit(self.sprite, (self.x - viewPort.x, self.y - viewPort.y))
            
