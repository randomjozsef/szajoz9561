import pygame
import random

pygame.init()

# Képernyő mérete
screen_width = 1027
screen_height = 847
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cubic Platformer")

# Színek
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
pink = (255, 0, 255)

# Karakter tulajdonságai
character_width = 50
character_height = 50
character_x = screen_width // 2 - character_width // 2
character_y = screen_height // 2 - character_height // 2

# Ajtók tulajdonságai
door_width = 50
door_height = 100

# Ajtók pozíciói
doors = {
    "top": (screen_width // 2 - door_width // 2, 0, door_width, door_height),  # Felső ajtó
    "bottom": (screen_width // 2 - door_width // 2, screen_height - door_height, door_width, door_height),  # Alsó ajtó
    "left": (0, screen_height // 2 - door_height // 2, door_height, door_width),  # Bal ajtó
    "right": (screen_width - door_height, screen_height // 2 - door_height // 2, door_height, door_width)  # Jobb ajtó
}

# Ugrás sebessége/mérete
speed = 0.5

# Szobák színei
room_colors = {
    1: black,
    2: blue,
    3: green,
    4: yellow,
    5: pink
}

# Véletlenszerű szoba-hozzárendelések
room_ids = [2, 3, 4, 5]  # Az 1-es szoba az induló szoba, a többi véletlenszerűen kerül hozzárendelésre
random.shuffle(room_ids)

# Szoba váltások az ajtók alapján
door_to_room = {
    1: {"top": room_ids[0], "bottom": room_ids[1], "left": room_ids[2], "right": room_ids[3]},
    room_ids[0]: {"bottom": 1},
    room_ids[1]: {"top": 1},
    room_ids[2]: {"right": 1},
    room_ids[3]: {"left": 1}
}

# Jelenlegi szoba
current_room = 1

# Játék működése
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

    # Ajtókkal való érintkezés ellenőrzése
    for door, (x, y, width, height) in doors.items():
        if (character_x < x + width and
            character_x + character_width > x and
            character_y < y + height and
            character_y + character_height > y):
            if door in door_to_room[current_room]:
                current_room = door_to_room[current_room][door]
                # Karaktert a képernyő közepére helyezzük minden szobaváltáskor
                character_x = screen_width // 2 - character_width // 2
                character_y = screen_height // 2 - character_height // 2

    # Képernyő frissítése
    screen.fill(room_colors[current_room])

    # Ajtók kirajzolása az aktuális szobában
    for x, y, width, height in doors.values():
        pygame.draw.rect(screen, red, (x, y, width, height))

    # Karakter kirajzolása
    pygame.draw.rect(screen, white, (character_x, character_y, character_width, character_height))
    pygame.display.update()

pygame.quit()