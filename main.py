import time

import pygame
import entity_handler
from pygame.constants import QUIT

pygame.init()

screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption('Basic Pygame program')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0, 10, 160))

entity_handler = entity_handler.EntityHandler(screen)

screen.blit(background, (0, 0))
pygame.display.flip()

clock = pygame.time.Clock()
endgame_display_timer = 180
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            entity_handler.firing = True
        if event.type == pygame.MOUSEBUTTONUP:
            entity_handler.firing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not entity_handler.reloading:
                entity_handler.to_reload = True

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 750, 1600, 150))
    for cannon in entity_handler.cannons:
        cannon.update()
    for shell in entity_handler.shells:
        shell.update()
    for plane in entity_handler.planes:
        plane.update()

    entity_handler.game_tick()

    text = pygame.font.Font(None, 50).render("HP left: " + str(entity_handler.player_hp), True, (255, 100, 100))
    screen.blit(text, (5, 10))

    text = pygame.font.Font(None, 38).render("Enemy planes: " + str(entity_handler.enemy_hp), True, (200, 80, 80))
    screen.blit(text, (screen.get_rect().centerx - text.get_width() / 2, text.get_height()))

    if entity_handler.player_hp <= 0:
        text = pygame.font.Font(None, 100).render("Game over", True, (100, 100, 100))
        screen.blit(text, (screen.get_rect().centerx - text.get_width() / 2, screen.get_rect().centery))
        pygame.display.flip()
        endgame_display_timer += -1
        if endgame_display_timer <= 0:
            running = False

    elif entity_handler.enemy_hp <=0:
        text = pygame.font.Font(None, 100).render("You win", True, (100, 100, 100))
        screen.blit(text, (screen.get_rect().centerx - text.get_width() / 2, screen.get_rect().centery))
        pygame.display.flip()
        endgame_display_timer += -1
        if endgame_display_timer <= 0:
            running = False

    pygame.display.flip()
