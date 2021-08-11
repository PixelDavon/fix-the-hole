import pygame, os
from random import randint as ri

pygame.init()

# Screen size
WIDTH, HEIGHT = 1200, 600

# Window
WIN = pygame.display.set_mode((WIDTH, HEIGHT),0)
# Title
pygame.display.set_caption('Fix the Hole')

# FPS
FPS = 60

# CUBE
CUBE_SIZE = 50
CUBEIMAGE = pygame.image.load(os.path.join('assets','cube.png'))
CUBEIMAGE = pygame.transform.scale(CUBEIMAGE, (CUBE_SIZE,CUBE_SIZE))

# WALL
WALL_RESCALE = 150
WALLIMAGE = pygame.image.load(os.path.join('assets','wall.png'))
WALLIMAGE = pygame.transform.scale(WALLIMAGE, (1710, 990-WALL_RESCALE))

# HOLES
HOLES = []
HOLEIMAGE = pygame.image.load(os.path.join('assets', 'hole.png'))

# Movement
VEL = 2

# Hole spawn chance
SPAWN_CHANCE = 150

# Key handler
def movement_handler(keys_pressed, cube_player: pygame.Rect):
    global VEL
    # Run
    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
        VEL = 10
    else:
        VEL = 2
    
    # General
    if keys_pressed[pygame.K_w]:
        cube_player.y-=VEL
    if keys_pressed[pygame.K_a]:
        cube_player.x-=VEL
    if keys_pressed[pygame.K_s]:
        cube_player.y+=VEL
    if keys_pressed[pygame.K_d]:
        cube_player.x+=VEL
    
    # collision
    if cube_player.x < 0:
        cube_player.x = 0
    if cube_player.x+CUBE_SIZE > WIN.get_width():
        cube_player.x=WIN.get_width()-CUBE_SIZE
    if cube_player.y < 0:
        cube_player.y = 0
    if cube_player.y+CUBE_SIZE > WIN.get_height():
        cube_player.y = WIN.get_height()-CUBE_SIZE

# Handle collision between hole and player
def handle_hole(HOLES: list, cube_player: pygame.Rect):
    for hole in HOLES:
        if cube_player.colliderect(hole):
            HOLES.remove(hole)

# Create hole
def generate_hole():
    global SPAWN_CHANCE

    # Append hole to a list
    holerect = HOLEIMAGE.get_rect(center=(ri(2,WIN.get_width()-50), ri(2, WIN.get_height()-50)))
    HOLES.append(holerect)

    # Change spawn chance
    if SPAWN_CHANCE > 120:
        if ri(1,10) == 10:
            SPAWN_CHANCE = int((SPAWN_CHANCE * 93) / 100)

    if 80 < SPAWN_CHANCE < 120:
        if ri(1,50) == 50:
            SPAWN_CHANCE = int((SPAWN_CHANCE * 95) / 100)

    if 40 < SPAWN_CHANCE < 80:
        if ri(1,100) == 100:
            SPAWN_CHANCE = int((SPAWN_CHANCE * 98) / 100)
    
    #print(SPAWN_CHANCE)


# Add objects to window
def drawstuff(cube_position: pygame.Rect, HOLES):
    # Fill everything with white cuz why not
    WIN.fill((255,255,255))

    # Add wall
    WIN.blit(WALLIMAGE, (0,0,WIN.get_width(),WIN.get_height()))
    # Add hole to screen
    for hole in HOLES:
        pygame.draw.rect(WIN, (0,0,0,0), hole)
    
    # Randomly create hole
    if ri(1,SPAWN_CHANCE) == SPAWN_CHANCE:
        generate_hole()
    
    # Add player to screen
    WIN.blit(CUBEIMAGE, cube_position)

    # Update
    pygame.display.update()

# Clock
clock = pygame.time.Clock()

# Main function
def main():
    # Player
    cube_player = CUBEIMAGE.get_rect(center=(WIN.get_width() //2,WIN.get_height() //2))
    
    # Self explanatory ._.
    run = True
    while run:
        # 60 FPS
        clock.tick(FPS)
        
        # Event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Get key pressed
        keys_pressed = pygame.key.get_pressed()

        # Call movement handler
        movement_handler(keys_pressed, cube_player)

        # Handle hole collision
        handle_hole(HOLES, cube_player)

        # Necessary objects
        drawstuff(cube_player, HOLES)
    pygame.quit()
if __name__ == '__main__':
    main()