import pygame
import network
import json

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
        self.player = pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 50, 50))


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
        self.player = pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 50, 50))

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
    
    
    
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    user = net.send("message:get")
    allUsers = net.send("message:get_all")
    allUsers = json.loads(allUsers)
    player, enemies = render_players(user, allUsers)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        net.send(f"message:update||{player.x - 5}:{player.y}:{player.health}:{player.rotation}")
    if keys[pygame.K_RIGHT]:
        net.send(f"message:update||{player.x + 5}:{player.y}:{player.health}:{player.rotation}")
    if keys[pygame.K_UP]:
        net.send(f"message:update||{player.x}:{player.y - 5}:{player.health}:{player.rotation}")
    if keys[pygame.K_DOWN]:
        net.send(f"message:update||{player.x}:{player.y + 5}:{player.health}:{player.rotation}")
    
    pygame.display.flip()

pygame.quit()
