import pygame
import network
import json
import math

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pew Pew")
clock = pygame.time.Clock()
running = True
net = network.Network()


class Player:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.health = 100
        self.rotation = 0

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.sprite = pygame.image.load("assets/player.png")
        self.player = pygame.transform.rotate(self.sprite, self.rotation)
        
        self.rect = self.player.get_rect()
        self.rect.x = self.x -int(self.player.get_width()/2)
        self.rect.y = int(self.y-self.player.get_height()/2)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.player.get_width(), self.player.get_height())
        screen.blit(self.player, self.hitbox)


class Enemy:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.health = 100
        self.rotation = 0

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.sprite = pygame.image.load("assets/enemy.png")
        self.player = pygame.transform.rotate(self.sprite, self.rotation)
        
        self.rect = self.player.get_rect()
        self.rect.x = self.x -int(self.player.get_width()/2)
        self.rect.y = int(self.y-self.player.get_height()/2)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, self.player.get_width(), self.player.get_height())
        screen.blit(self.player, self.hitbox)


def render_players(player, enemies):
    _player = Player(player.split("||")[1].split(":")[1])
    vals = {}
    for key in player.split("||"):
        try:
            vals[key.split(":")[0]] = int(key.split(":")[1])
        except:
            vals[key.split(":")[0]] = key.split(":")[1]
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
            _enemies[-1].update(**_val)
    return _player, _enemies

def get_rotation(player_pos: list):
    cursor_pos = list(pygame.mouse.get_pos())
    return int(math.atan2(player_pos[0] - cursor_pos[0],  player_pos[1]-cursor_pos[1]) * 180 / math.pi)

while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((12, 151, 0))

    user = net.send("message:get")
    allUsers = net.send("message:get_all")
    allUsers = json.loads(allUsers)
    player, enemies = render_players(user, allUsers)
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

    pygame.display.flip()

pygame.quit()
