import pygame
import network
import json
import math
from objects import Player, Enemy, Bullet

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 640))
pygame.display.set_caption("Pew Pew")
clock = pygame.time.Clock()
running = True
net = network.Network()
mapdata = net.send("message:get_map")


def render_players(player, enemies) -> (Player, []):
    _player = Player(player.split("||")[1].split(":")[1])
    vals = {}
    for key in player.split("||"):
        try:
            vals[key.split(":")[0]] = int(key.split(":")[1])
        except:
            vals[key.split(":")[0]] = key.split(":")[1]
    vals['screen'] = screen
    _player.update(**vals)

    _enemies = []
    for user_ in allUsers.values():
        if user_.split("||")[0].split(":")[1] != player.split("||")[0].split(":")[1]:
            _val = {}
            _enemies.append(Enemy(user_.split("||")[1].split(":")[1]))
            for key in user_.split("||"):
                try:
                    _val[key.split(":")[0]] = int(key.split(":")[1])
                except:
                    _val[key.split(":")[0]] = key.split(":")[1]
            _val['screen'] = screen
            _enemies[-1].update(**_val)
    return _player, _enemies


def get_rotation(player_pos: list) -> int:
    cursor_pos = list(pygame.mouse.get_pos())
    return int(
        math.atan2(player_pos[0] - cursor_pos[0], player_pos[1] - cursor_pos[1])
        * 180
        / math.pi
    )


def render_map() -> None:
    screen.fill((12, 151, 0))
    gameMap = json.loads(mapdata)
    walls = pygame.image.load("assets/map/wall.png")
    x, y = 0, 0
    for i in gameMap:
        for k in i:
            if k == 1:
                screen.blit(walls, (x, y))
            x += 32
        x = 0
        y += 32


allBullets = []
allUsers = net.send("message:get_all")
allUsers = json.loads(allUsers)
user = net.send("message:get")
player, enemies = render_players(user, allUsers)


while running:
    # global allUsers, user
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    render_map()
    user = net.send("message:get")
    try:
        allUsers = net.send("message:get_all")
        allUsers = json.loads(allUsers)
        player, enemies = render_players(user, allUsers)
    except Exception as e:
        # pass
        print(e)
    player.rotation = get_rotation([player.x, player.y])
    net.send(f"message:update||{player.x}:{player.y}:{player.health}:{player.rotation}")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        net.send(
            f"message:update||{player.x - 5}:{player.y}:{player.health}:{player.rotation}"
        )
    if keys[pygame.K_RIGHT]:
        net.send(
            f"message:update||{player.x + 5}:{player.y}:{player.health}:{player.rotation}"
        )
    if keys[pygame.K_UP]:
        net.send(
            f"message:update||{player.x}:{player.y - 5}:{player.health}:{player.rotation}"
        )
    if keys[pygame.K_DOWN]:
        net.send(
            f"message:update||{player.x}:{player.y + 5}:{player.health}:{player.rotation}"
        )
    # if mouse left click
    if pygame.mouse.get_pressed()[0]:
        net.send(f"message:shoot||{player.x}:{player.y}")
        # allBullets.append(Bullet(player.x, player.y, player.id))
    print(len(allBullets))
    for bullet in allBullets:
        if bullet.x > 800 or bullet.x < 0 or bullet.y > 616 or bullet.y < 0:
            allBullets.remove(bullet)
        bullet.update()

    pygame.display.flip()

pygame.quit()
