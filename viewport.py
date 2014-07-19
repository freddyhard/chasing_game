

class ViewPort():
    def __init__(self, player, vp_width, vp_height):
        self.x = player.x + 25 - vp_width / 2
        self.y = player.y + 25 - vp_height / 2
        self.width = vp_width
        self.height = vp_height
        
    
    
    
    def move(self, player, map_width, map_height):
        self.x = player.x + 25 - self.width / 2 
        self.y = player.y + 25 - self.height / 2
        
        if self.x + self.width > map_width:
            self.x = map_width - self.width
        elif self.x < 0:
            self.x = 0
        if self.y + self.height > map_height:
            self.y = map_height - self.height
        elif self.y < 0:
            self.y = 0
        
