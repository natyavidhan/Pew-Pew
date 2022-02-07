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

while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    
    user = net.send("message:get")
    # print(user)
    allUsers = net.send("message:get_all")
    allUsers = json.loads(allUsers)
    print(allUsers)
    pygame.display.flip()       

pygame.quit()