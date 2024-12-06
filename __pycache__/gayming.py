import pygame
import random
import time

pygame.init()

# Képernyő mérete
screen_width = 1027
screen_height = 847
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cubic Platformer")

# Színek
white = (255, 255, 255)
red = (255, 0, 0)
room_colors = {
    i: (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    for i in range(1, 257)  # 16x16 = 256 szoba
}

# Karakter tulajdonságai
character_width = 50
character_height = 50
character_x = screen_width // 2 - character_width // 2
character_y = screen_height // 2 - character_height // 2
speed = 0.5

# Ajtók tulajdonságai
door_width = 50
door_height = 100
doors = {
    "top": (screen_width // 2 - door_width // 2, 0, door_width, door_height),
    "bottom": (screen_width // 2 - door_width // 2, screen_height - door_height, door_width, door_height),
    "left": (0, screen_height // 2 - door_height // 2, door_height, door_width),
    "right": (screen_width - door_height, screen_height // 2 - door_height // 2, door_height, door_width),
}

# 16x16 szobák inicializálása
room_connections = {room_id: {} for room_id in range(1, 257)}

# 16x16 szobák ajtókapcsolatai
for y in range(16):
    for x in range(16):
        room_id = y * 16 + x + 1

        # Véletlenszerű ajtók generálása a szomszédos szobák között
        if y > 0 and random.choice([True, False]):  # Felső szoba
            top_room = (y - 1) * 16 + x + 1
            room_connections[room_id]["top"] = top_room
            room_connections[top_room]["bottom"] = room_id

        if y < 15 and random.choice([True, False]):  # Alsó szoba
            bottom_room = (y + 1) * 16 + x + 1
            room_connections[room_id]["bottom"] = bottom_room
            room_connections[bottom_room]["top"] = room_id

        if x > 0 and random.choice([True, False]):  # Bal szoba
            left_room = y * 16 + (x - 1) + 1
            room_connections[room_id]["left"] = left_room
            room_connections[left_room]["right"] = room_id

        if x < 15 and random.choice([True, False]):  # Jobb szoba
            right_room = y * 16 + (x + 1) + 1
            room_connections[room_id]["right"] = right_room
            room_connections[right_room]["left"] = room_id

# Lövedékek kezelése
bullets = []
last_shot_time = 0
shot_cooldown = 0.5  # Másodperc

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.size = 10

    def move(self):
        if self.direction == "left":
            self.x -= 5
        elif self.direction == "right":
            self.x += 5
        elif self.direction == "up":
            self.y -= 5
        elif self.direction == "down":
            self.y += 5

    def draw(self, screen):
        pygame.draw.rect(screen, red, (self.x, self.y, self.size, self.size))

# Jelenlegi szoba
current_room = 1

# Minimap tulajdonságai
minimap_width = 200
minimap_height = 200
minimap_x = 10
minimap_y = 10

# Játék fő ciklusa
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Karakter mozgása
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x -= speed
        if character_x < 0:
            character_x = 0
    if keys[pygame.K_RIGHT]:
        character_x += speed
        if character_x > screen_width - character_width:
            character_x = screen_width - character_width
    if keys[pygame.K_UP]:
        character_y -= speed
        if character_y < 0:
            character_y = 0
    if keys[pygame.K_DOWN]:
        character_y += speed
        if character_y > screen_height - character_height:
            character_y = screen_height - character_height

    # Lövések kezelése
    current_time = time.time()
    if current_time - last_shot_time > shot_cooldown:
        if keys[pygame.K_a]:  # Balra
            bullets.append(Bullet(character_x, character_y + character_height // 2 - 5, "left"))
            last_shot_time = current_time
        if keys[pygame.K_d]:  # Jobbra
            bullets.append(Bullet(character_x + character_width, character_y + character_height // 2 - 5, "right"))
            last_shot_time = current_time
        if keys[pygame.K_w]:  # Felfelé
            bullets.append(Bullet(character_x + character_width // 2 - 5, character_y, "up"))
            last_shot_time = current_time
        if keys[pygame.K_s]:  # Lefelé
            bullets.append(Bullet(character_x + character_width // 2 - 5, character_y + character_height, "down"))
            last_shot_time = current_time

    # Bullet mozgás
    for bullet in bullets[:]:
        bullet.move()
        if bullet.x < 0 or bullet.x > screen_width or bullet.y < 0 or bullet.y > screen_height:
            bullets.remove(bullet)

    # Ajtókkal való érintkezés ellenőrzése
    for door, (x, y, width, height) in doors.items():
        if door in room_connections[current_room] and (
            character_x < x + width and
            character_x + character_width > x and
            character_y < y + height and
            character_y + character_height > y):
            current_room = room_connections[current_room][door]
            character_x = screen_width // 2 - character_width // 2
            character_y = screen_height // 2 - character_height // 2

    # Képernyő frissítése
    screen.fill(room_colors[current_room])

    # Ajtók kirajzolása
    for door, (x, y, width, height) in doors.items():
        if door in room_connections[current_room]:
            pygame.draw.rect(screen, white, (x, y, width, height))

    # Karakter kirajzolása
    pygame.draw.rect(screen, white, (character_x, character_y, character_width, character_height))

    # Lövedékek kirajzolása
    for bullet in bullets:
        bullet.draw(screen)

    # Minimap kirajzolása
    pygame.draw.rect(screen, white, (minimap_x, minimap_y, minimap_width, minimap_height), 2)  # Minimap keret
    minimap_scale = minimap_width / 16  # A minimap mérete, 16x16 szoba
    for y in range(16):
        for x in range(16):
            room_id = y * 16 + x + 1
            if room_id in room_connections:  # Ha van kapcsolat
                room_rect = pygame.Rect(minimap_x + x * minimap_scale, minimap_y + y * minimap_scale,
                                        minimap_scale, minimap_scale)
                pygame.draw.rect(screen, room_colors[room_id], room_rect)

    # A játékos pozíciójának ábrázolása a minimapon
    player_minimap_x = minimap_x + (current_room % 16) * minimap_scale
    player_minimap_y = minimap_y + (current_room // 16) * minimap_scale
    pygame.draw.rect(screen, red, (player_minimap_x, player_minimap_y, minimap_scale, minimap_scale))

    pygame.display.update()

pygame.quit()
