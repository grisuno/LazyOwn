import pygame
import os


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480  
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mario Bros 1-1 Clone")
clock = pygame.time.Clock()


FONT_PATH = os.path.join(os.path.dirname(__file__), "NotoEmoji-Regular.ttf")
if not os.path.exists(FONT_PATH):
    print("Error: 'NotoEmoji-Regular.ttf' no encontrado.")
    print("1. Descarga la fuente desde: https://fonts.google.com/noto/specimen/Noto+Emoji")
    print("2. Guarda 'NotoEmoji-Regular.ttf' en el mismo directorio que este script.")
    print("Usando fuente predeterminada como fallback (emojis no se mostrarán correctamente).")
    FONT = pygame.font.SysFont("arial", 32)  
else:
    FONT = pygame.font.Font(FONT_PATH, 32)


MARIO = "🏃"
BLOCK = "🧱"
PIPE = "🚪"
GOOMBA = "👾"
TURTLE = "🐢"
GROUND = "⬜"
SKY = "  "
CLOUD = "☁️"
BUSH = "🌳"
MOUNTAIN = "🏔️"
COIN = "🪙"
BRICK = "🟫"
FLAGPOLE = "🏁"
CASTLE = "🏰"
SUN = "☀️"
FLOWER = "🌸"
TREE = "🌲"


TILE_SIZE = 32
LEVEL_WIDTH = 150 * TILE_SIZE
LEVEL_HEIGHT = 15 * TILE_SIZE


BACKGROUND = [[SKY] * (LEVEL_WIDTH // TILE_SIZE) for _ in range(LEVEL_HEIGHT // TILE_SIZE)]
MIDDLEGROUND = [[SKY] * (LEVEL_WIDTH // TILE_SIZE) for _ in range(LEVEL_HEIGHT // TILE_SIZE)]
FOREGROUND = [[SKY] * (LEVEL_WIDTH // TILE_SIZE) for _ in range(LEVEL_HEIGHT // TILE_SIZE - 1)] + [[GROUND] * (LEVEL_WIDTH // TILE_SIZE)]


BACKGROUND[1][5] = SUN
BACKGROUND[2][20] = CLOUD
BACKGROUND[3][50] = CLOUD
BACKGROUND[4][100] = CLOUD
MIDDLEGROUND[8][10] = MOUNTAIN
MIDDLEGROUND[9][40] = MOUNTAIN
MIDDLEGROUND[7][90] = MOUNTAIN
MIDDLEGROUND[13][15] = TREE
MIDDLEGROUND[13][60] = BUSH
MIDDLEGROUND[13][110] = TREE
FOREGROUND[11][10] = BRICK
FOREGROUND[11][11] = BLOCK
FOREGROUND[11][12] = BRICK
FOREGROUND[10][20] = COIN
FOREGROUND[9][25] = COIN
FOREGROUND[9][30] = PIPE
FOREGROUND[13][35] = GOOMBA
FOREGROUND[12][40] = FLOWER
FOREGROUND[11][50] = BRICK
FOREGROUND[11][51] = BLOCK
FOREGROUND[7][60] = PIPE
FOREGROUND[13][70] = TURTLE
FOREGROUND[12][80] = BUSH
FOREGROUND[13][90] = GOOMBA
FOREGROUND[11][100] = COIN
FOREGROUND[13][130] = FLAGPOLE
FOREGROUND[12][135] = CASTLE


mario_x = 2 * TILE_SIZE
mario_y = (LEVEL_HEIGHT // TILE_SIZE - 2) * TILE_SIZE  
mario_vx = 0.0
mario_vy = 0.0
GRAVITY = 500.0
JUMP_SPEED = -300.0
MAX_VX = 200.0
ACCEL = 800.0
FRICTION = 600.0
enemies = [
    {"x": 35 * TILE_SIZE, "vx": -50.0, "type": GOOMBA},
    {"x": 70 * TILE_SIZE, "vx": -30.0, "type": TURTLE},
    {"x": 90 * TILE_SIZE, "vx": -50.0, "type": GOOMBA}
]
camera_x = 0
score = 0
coins = 0

def check_collision(x, y, layer=FOREGROUND):
    x_tile = int(x // TILE_SIZE)
    y_tile = int(y // TILE_SIZE)
    if 0 <= x_tile < LEVEL_WIDTH // TILE_SIZE and 0 <= y_tile < LEVEL_HEIGHT // TILE_SIZE:
        tile = layer[y_tile][x_tile]
        if tile in (BLOCK, PIPE, BRICK):
            return "solid"
        elif tile == COIN:
            layer[y_tile][x_tile] = SKY
            global score, coins
            score += 100
            coins += 1
            return None
        return None
    return "out"


running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False

    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        mario_vx = min(mario_vx + ACCEL * dt, MAX_VX * (2 if keys[pygame.K_LALT] else 1))
    elif keys[pygame.K_LEFT]:
        mario_vx = max(mario_vx - ACCEL * dt, -MAX_VX * (2 if keys[pygame.K_LALT] else 1))
    else:
        if mario_vx > 0:
            mario_vx = max(mario_vx - FRICTION * dt, 0)
        elif mario_vx < 0:
            mario_vx = min(mario_vx + FRICTION * dt, 0)
    if keys[pygame.K_SPACE] and abs(mario_y - (LEVEL_HEIGHT // TILE_SIZE - 2) * TILE_SIZE) < 5:
        mario_vy = JUMP_SPEED

    
    mario_vy += GRAVITY * dt
    next_x = mario_x + mario_vx * dt
    next_y = mario_y + mario_vy * dt

    
    collision = check_collision(next_x, mario_y)
    if collision == "solid":
        mario_vx = 0
        mario_x = int(next_x / TILE_SIZE) * TILE_SIZE + (TILE_SIZE if mario_vx < 0 else 0)
    elif collision != "out":
        mario_x = next_x

    
    collision = check_collision(mario_x, next_y)
    if collision == "solid":
        if mario_vy > 0:
            mario_y = int(next_y / TILE_SIZE) * TILE_SIZE - 0.001
            mario_vy = 0
        elif mario_vy < 0:
            mario_y = (int(next_y / TILE_SIZE) + 1) * TILE_SIZE
            mario_vy = 0
    elif collision != "out":
        mario_y = next_y

    
    ground_level = (LEVEL_HEIGHT // TILE_SIZE - 2) * TILE_SIZE
    if mario_y >= ground_level:
        mario_y = ground_level
        mario_vy = 0
    if mario_x < 0:
        mario_x = 0

    
    camera_x = max(0, min(mario_x - SCREEN_WIDTH // 2, LEVEL_WIDTH - SCREEN_WIDTH))

    
    for enemy in enemies:
        enemy["x"] += enemy["vx"] * dt
        if check_collision(enemy["x"], ground_level / TILE_SIZE) == "solid" or enemy["x"] < 0 or enemy["x"] >= LEVEL_WIDTH:
            enemy["vx"] *= -1

    
    screen.fill((135, 206, 235))  
    for y in range(LEVEL_HEIGHT // TILE_SIZE):
        for x in range(LEVEL_WIDTH // TILE_SIZE):
            bg_x = x * TILE_SIZE - int(camera_x * 0.2)
            mg_x = x * TILE_SIZE - int(camera_x * 0.5)
            fg_x = x * TILE_SIZE - int(camera_x)
            if -TILE_SIZE <= fg_x < SCREEN_WIDTH + TILE_SIZE:
                for layer, scroll_x in [(BACKGROUND, bg_x), (MIDDLEGROUND, mg_x), (FOREGROUND, fg_x)]:
                    tile = layer[y][x]
                    if tile != SKY:
                        text = FONT.render(tile, True, (0, 0, 0))
                        screen.blit(text, (scroll_x, y * TILE_SIZE))

    
    screen.blit(FONT.render(MARIO, True, (0, 0, 0)), (mario_x - camera_x, mario_y))
    for enemy in enemies:
        screen.blit(FONT.render(enemy["type"], True, (0, 0, 0)), (enemy["x"] - camera_x, ground_level))

    
    score_text = FONT.render(f"Score: {score}  Coins: {coins}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    
    for enemy in enemies:
        if abs(mario_x - enemy["x"]) < TILE_SIZE and abs(mario_y - ground_level) < TILE_SIZE:
            running = False

    pygame.display.flip()

pygame.quit()