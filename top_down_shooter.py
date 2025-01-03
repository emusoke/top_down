import pygame
import socket
import json
import sys

HOST = "localhost"
PORT = 12000


def get_opp(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message)
        message = s.recv(1024)

    opp_position = message.decode()
    opp_position_dict = json.loads(opp_position)
    return opp_position_dict


# Example file showing a circle moving on screen
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 3, screen.get_height() / 2)
player_two_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

player_id = sys.argv[1]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    if player_id == "1":
        screen.fill("green")
    else:
        screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)
    pygame.draw.circle(screen, "blue", player_two_pos, 40)

    keys = pygame.key.get_pressed()

    if player_id == "1":
        controlling_player = player_pos
        oppostion_player = player_two_pos
    else:
        controlling_player = player_two_pos
        oppostion_player = player_pos

    if keys[pygame.K_w]:
        controlling_player.y -= 300 * dt
    if keys[pygame.K_s]:
        controlling_player.y += 300 * dt
    if keys[pygame.K_a]:
        controlling_player.x -= 300 * dt
    if keys[pygame.K_d]:
        controlling_player.x += 300 * dt

    player_pos_dict = {"player_id": player_id,
                       "x": controlling_player.x,
                       "y": controlling_player.y
                       }

    message = json.dumps(player_pos_dict).encode("utf-8")
    opposition_update = get_opp(message)

    oppostion_player.x = opposition_update["x"]
    oppostion_player.y = opposition_update["y"]

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
