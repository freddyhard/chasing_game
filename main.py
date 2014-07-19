import pygame, sys, glob, os
from random import randint

from t800 import T800
from mapsection import MapSection
from viewport import ViewPort
from t1000 import T1000
from console import Console
from people import People

from functions import removeDestroyed, vector

#-------------------------------------------------------------------------------
#                                 GAME PARAMETERS
#-------------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 560
DISPLAY_PANEL = 40
FPS = 40
MAP_WIDTH = 4000
MAP_HEIGHT = 4000
#-------------------------------------------------------------------------------
#                                   FUNCTIONS
#-------------------------------------------------------------------------------
def createGroup():
    # declare a 2D array for the different groups that the people can be organised into
    scatter = [[(0,0) for x in range(8)]for x in range(5)]
    
    
    # i put these positions together using a graphic editor to position the sprites in a group
    scatter[0] = ((12,34), (255,34), (133,91), (73,161), (255,179), (184,229), (23,266), (111,266))
    scatter[1] = ((12,7), (103,18), (48,104), (128,117), (273,141), (36,196), (128,263), (36,275))
    scatter[2] = ((59,60), (130,85), (22,135), (92,148), (143,203), (46,216), (274,117), (271,215))
    scatter[3] = ((188,40), (100,97), (187,129), (137,203), (87,267), (201,271), (302,153), (0,153))
    scatter[4] = ((0,0), (0,301), (300,303), (300,0), (187,79), (74,104), (99,191), (212,217))
    
    # select a random row for the group
    randomRow = randint(0, len(scatter) - 1)
    
    # select a random y position for this group.
    randomY = randint(500, MAP_HEIGHT - 500)
    
    # all in the group will be placed at their x position -350 to place them at the left side of the map
    for f in range(8):
        (x, y) = scatter[randomRow][f]
        # 1:6 chance to create terminator
        if randint(0, 5) == 0:
            terminators.append(T800(x - 350, y + randomY, MAP_WIDTH + 50, y + randomY, MAP_WIDTH, MAP_HEIGHT))
        else:
            people.append(People(x - 350, y + randomY, MAP_WIDTH + 50, y + randomY, MAP_WIDTH, MAP_HEIGHT))
    

def keyCheck():
    global gamePaused, gamePlaying
    
    for gameEvent in pygame.event.get():
        if (gameEvent.type == pygame.QUIT):
            sys.exit()
        
        # CHANGE RADAR RANGE
        if (gameEvent.type == pygame.MOUSEBUTTONDOWN and gamePlaying):
            if (gameEvent.button == 4 and console.radarRange > 800):
                console.radarRange -= 400
            elif (gameEvent.button == 5 and console.radarRange < 2000):
                console.radarRange += 400
        
        if (gameEvent.type == pygame.KEYDOWN):
            # QUIT
            if (gameEvent.key == pygame.K_ESCAPE):
                sys.exit()
            if gamePlaying:
                # PAUSE (only when player is alive)
                if (gameEvent.key == pygame.K_PAUSE):# and player.armour > 0):
                    gamePaused = not gamePaused
            else:
                # RESET THE GAME
                if (gameEvent.key == pygame.K_SPACE):# and player.armour == 0):
                    clearGroups()
                    player.reinit()
                    gamePlaying = True
                    
                    
def clearGroups():
    global people, terminators
    
    # declare new arrays for both
    people = []
    terminators = []
    



def draw():
    # draw the background map
    for f in range(len(gameMap)):
        gameMap[f].draw(window, player_ViewPort)
        

    # draw civilians
    for f in range(len(people)):
        people[f].draw(window, player_ViewPort)
    
    # draw rogue T800s
    for f in range(len(terminators)):
        terminators[f].draw(window, player_ViewPort)
    
    # draw lasers
    for f in range(len(lasers)):
        lasers[f].draw(window, player_ViewPort)
    
    if gamePlaying or gameOverDisplay != 0:
        # draw player
        player.draw(window, player_ViewPort)
        if not gamePlaying or gamePaused:
            window.blit(darkenRect, (0,0))
    else:
        window.blit(darkenRect, (0,0))
    
    # draw radar (last to fill up the bottom bit of the screen)
    console.draw(window, player)



def demoMode():
    global gamePlaying
    
    # a timer to display the start game key
    flashTimer = 0
    
    # downloaded from mp3skull.com
    titleMusic = pygame.mixer.Sound(os.path.join("sounds", "b_music.ogg"))
    titleMusic.set_volume(0.3)
    titleMusic.play()
    
    # set the font for display
    messageFont = pygame.font.Font(os.path.join("fonts", "keypuncn.ttf"), 22)
    
    clearGroups()
    
    # build an array of text for easy displaying on the screen
    instructions = []
    instructions.append("A long long time ago,  some where in the future...  well there was a lot")
    instructions.append("of time travelling going on,  but ended up in the future and computers")
    instructions.append("have taken over the world despite what the programmers said.")
    instructions.append("You are a T800 and have been programmed to encourage the few")
    instructions.append("remaining humans to retire.")
    instructions.append("")
    instructions.append("One hit from your automatic laser blaster pistol and they will")
    instructions.append("disintegrate.  What kind of retirement were you thinking of ?")
    instructions.append("Unfortunately there are other T800's that have been reprogrammed")
    instructions.append("to protect them.  They will need early retirement as well.")
    instructions.append("")
    instructions.append("Use the mouse to point yourself in any direction and the arrow keys")
    instructions.append("to move in that direction.  You cannot run forwards/backwards and side")
    instructions.append("step at the same time.  The T800-b only has that control chip.")
    instructions.append("Use the roller mouse to change the radar range.")
    instructions.append("Hold down left mouse to fire.")
    instructions.append("'PAUSE'  will pause the game.")
    
    textStart = messageFont.render("p r e s s    s p a c e    t o    s t a r t", 1, (255,100,50))
    
    # continuous loop goes in here moving player in straight lines, but not drawing him
    player.x = MAP_WIDTH / 2
    player.y = MAP_HEIGHT / 2
    
    (pan_x, pan_y) = vector(randint(0, 359), 0.6)
    
    while (not gamePlaying):
        # keep a count of the frames per second
        gameTimer.tick(FPS)
        # increment the blink timer keeping it to 1 second limit
        flashTimer = (flashTimer + 1) % FPS
        # move the player so that the view port will pan around the map
        player.x += pan_x
        player.y += pan_y
        
        # bounce the view as it pans towards the map edge
        if player.x > 3500 or player.x < 500:
            pan_x = -pan_x
        if player.y > 3500 or player.y < 500:
            pan_y = -pan_y
        
        # move the view port
        player_ViewPort.move(player, MAP_WIDTH, MAP_HEIGHT)
        # update the console
        console.move(people, terminators, player)
        # draw everything
        draw()
        
        # display the instructions
        for f in range(len(instructions)):
            text = messageFont.render(instructions[f], 1, colourYellow)
            window.blit(text, (40, 25 + f * 28))
        
        # every half a second will blink
        if flashTimer < FPS / 2:
            window.blit(textStart, (SCREEN_WIDTH / 2 - text.get_width() / 2, 520))
        
        # check the keyboard
        keyCheck()
        
        pygame.display.flip()
    
    titleMusic.stop()
    

#-------------------------------------------------------------------------------
#                                 INITIALISE GAME
#-------------------------------------------------------------------------------

# the pre_init was needed to avoid sound delays for some reason
pygame.mixer.pre_init(44100, -16, 16, 4096)

# initialise the game
pygame.init()

# declare the window size
pygame.display.set_icon(pygame.image.load(os.path.join("sprites", "icon.png")))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + DISPLAY_PANEL))
pygame.display.set_caption("Terminator")

gameTimer = pygame.time.Clock()

# hide the OS pointer
pygame.mouse.set_visible(False)

# this sprite will be used instead of the OS pointer
cursorSprite = pygame.image.load(os.path.join("sprites", "cursor.png"))

# a rectangle to darken the background while displaying instructions, pausing the game or game over
darkenRect = pygame.image.load(os.path.join("sprites", "darkRectangle.png")).convert_alpha()

gamePaused = False
gamePlaying = False
# a timer to display the game over message
gameOverDisplay = 0

# defining my preferred yellow colour
colourYellow = (255,240,0)

# font sizes
gameOverFont = pygame.font.Font(os.path.join("fonts", "keypuncn.ttf"), 60)
pressSpaceFont = pygame.font.Font(os.path.join("fonts", "keypuncn.ttf"), 30)
gamePausedFont = pygame.font.Font(os.path.join("fonts", "keypuncn.ttf"), 40)


# load the map images into an array
mapSprite = glob.glob(os.path.join("sprites", "map", "map_*.jpg"))

# declare an array that will hold objects from the class MapSection
gameMap = []
for row in range(4):
    for col in range(4):
        # each object gets a piece of the map to display
        gameMap.append(MapSection(col * 1000, row * 1000, mapSprite[col + 4 * row]))

# clear this array now - no longer needed since sprites were passed into objects above
mapSprite = []

# the player
player = T1000(3500, 2000, MAP_WIDTH, MAP_HEIGHT)
player_ViewPort = ViewPort(player, SCREEN_WIDTH, SCREEN_HEIGHT)

#display 
console = Console()

# declare arrays of objects for game play
people = []
terminators = []
lasers = []


# main game loop
while (True):
    
    # keep a count of the frames per second 
    gameTimer.tick(FPS)
    
    # if this timer has been set then decrement it
    if gameOverDisplay > 0:
        gameOverDisplay -= 1
    
    # if the game has ended and the message displayed to the player is finished enter the demo mode    
    if not gamePlaying and gameOverDisplay == 0:
        demoMode()
    
    # once the player's armour > 0 the game is playing
    gamePlaying = (player.armour > 0)
    
    # check the keyboard
    keyCheck()
    
    
    if not gamePaused:
        # move player
        player.move(player_ViewPort, lasers)
        # update the viewport
        player_ViewPort.move(player, MAP_WIDTH, MAP_HEIGHT)
        
        # create a new group when civilians = 0
        if len(people) == 0:
            createGroup()

        # update the display area
        console.move(people, terminators, player)
        
        # cycle through the move() for the arrays lasers, people and terminators
        for f in range(len(lasers)):
            lasers[f].move(player, people, terminators)
            
        for f in range(len(people)):
            people[f].move(player)
        
        for f in range(len(terminators)):
            terminators[f].move(player, lasers)
        
        # remove any objects that have their attribute destroyed = true
        lasers = removeDestroyed(lasers)
        people = removeDestroyed(people)
        terminators = removeDestroyed(terminators)
    
    
    # draw all the objects
    draw()
    
    # display game over for the player
    if player.armour == 0:
        if gameOverDisplay == 0:
            gameOverDisplay = 240
            
        gameOverText = gameOverFont.render("BATTERIES  DEPLETED", 1, colourYellow)
        window.blit(gameOverText, (SCREEN_WIDTH / 2 - gameOverText.get_width() / 2, SCREEN_HEIGHT / 2))
        
        pressSpaceText = pressSpaceFont.render("press space to restart", 1, colourYellow)
        window.blit(pressSpaceText, (SCREEN_WIDTH / 2 - pressSpaceText.get_width() / 2, SCREEN_HEIGHT / 2 + 100))
    
    if gamePaused:
        #fontArial = pygame.font.SysFont('arial', 18, True, False)
        gamePausedText = gamePausedFont.render("P A U S E D", 1, (255,255,255))
        
        window.blit(gamePausedText, (SCREEN_WIDTH / 2 - gamePausedText.get_width() / 2, SCREEN_HEIGHT / 2 + 100))
    
    mouse_pos = pygame.mouse.get_pos()
    window.blit(cursorSprite, (mouse_pos[0] - 16, mouse_pos[1] - 16))
    pygame.display.flip()







