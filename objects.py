import math, pygame

class Player:
    def __init__(self, id):
        self.id = id
        self.x = 0
        self.y = 0
        self.health = 100
        self.rotation = 0
        self.screen = None

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.sprite = pygame.image.load("assets/player.png")
        self.player = pygame.transform.rotate(self.sprite, self.rotation)

        self.rect = self.player.get_rect()
        self.rect.x = self.x - int(self.player.get_width() / 2)
        self.rect.y = int(self.y - self.player.get_height() / 2)
        self.hitbox = pygame.Rect(
            self.rect.x, self.rect.y, self.player.get_width(), self.player.get_height()
        )
        self.screen.blit(self.player, self.hitbox)

        self.playerData = f"{self.id} [{self.health}]"
        self.playerText = pygame.font.SysFont("comicsans", 20).render(
            self.playerData, 1, (255, 255, 255)
        )
        self.playerTextRect = self.playerText.get_rect()
        self.playerTextRect.center = (self.x, self.y)
        self.playerTextRect.x -= int(self.playerText.get_width() / 12)
        self.playerTextRect.y -= int(self.playerText.get_height())
        self.DataHitbox = pygame.Rect(
            self.playerTextRect.x,
            self.playerTextRect.y,
            self.playerText.get_width(),
            self.playerText.get_height(),
        )
        self.screen.blit(self.playerText, self.playerTextRect)


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
        self.rect.x = self.x - int(self.player.get_width() / 2)
        self.rect.y = int(self.y - self.player.get_height() / 2)
        self.hitbox = pygame.Rect(
            self.rect.x, self.rect.y, self.player.get_width(), self.player.get_height()
        )
        self.screen.blit(self.player, self.hitbox)

        self.playerData = f"{self.id} [{self.health}]"
        self.playerText = pygame.font.SysFont("comicsans", 20).render(
            self.playerData, 1, (255, 255, 255)
        )
        self.playerTextRect = self.playerText.get_rect()
        self.playerTextRect.center = (self.x, self.y)
        self.playerTextRect.x -= int(self.playerText.get_width() / 12)
        self.playerTextRect.y -= int(self.playerText.get_height())
        self.DataHitbox = pygame.Rect(
            self.playerTextRect.x,
            self.playerTextRect.y,
            self.playerText.get_width(),
            self.playerText.get_height(),
        )
        self.screen.blit(self.playerText, self.playerTextRect)