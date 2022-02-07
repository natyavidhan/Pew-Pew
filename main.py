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


while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))

    user = net.send("message:get")
    player = Player(user.split("||")[1].split(":")[1])
    vals = {}
    for key in user.split("||"):
        try:
            vals[key.split(":")[0]] = int(key.split(":")[1])
        except:
            vals[key.split(":")[0]] = key.split(":")[1]
    player.update(**vals)
    # print(user)
    allUsers = net.send("message:get_all")
    allUsers = json.loads(allUsers)
    enemies = []
    for user_ in allUsers.values():
        if user_.split("||")[0].split(":")[1] != user.split("||")[0].split(":")[1]:
            _val = {}
            enemies.append(Enemy(user_.split("||")[1].split(":")[1]))
            for key in user_.split("||"):
                try:
                    _val[key.split(":")[0]] = int(key.split(":")[1])
                except:
                    _val[key.split(":")[0]] = key.split(":")[1]
            enemies[-1].update(**_val)
    print(allUsers)
    pygame.display.flip()

pygame.quit()
