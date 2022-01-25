import math
import random

import pygame.font

import entities


class EntityHandler:
    cannon_ammo = 4
    reload_time = 120

    def __init__(self, screen):
        self.spawn_ticker = 180
        self.screen = screen
        self.plane_size = entities.Plane(screen, 0, 0).rect.width
        self.planes = []
        self.cannons = []
        self.shells = []
        self.player_hp = 12
        self.enemy_hp = 0
        self.firing = False
        self.current_ammo = 4
        self.reload_left = 0
        self.to_reload = False
        self.reloading = False
        self.planes_iterator = iter(self.planes)

        for i in range(1, 5):
            self.cannons.append(entities.Cannon(screen, (320 * i - 25), 800))
        for i in range(0, 14):
            self.planes.append(entities.Plane(screen, random.randint(0, 1600 - self.plane_size), 0))
            self.enemy_hp += 4

    def game_tick(self):
        self.spawn_plane()

        self.display_ammo()

        if self.to_reload or self.current_ammo == 0:
            self.start_reload()
        self.reload()

        for plane in self.planes:
            if plane.hp <= 0:
                self.planes.remove(plane)
            if plane.rect.y > 900:
                self.player_hp += -plane.bombing_run()
            if plane.rect.y < 0:
                plane.active = False
                plane.rearm()
            if plane.rect.x > 1600 or plane.rect.x < 0:
                self.planes.remove(plane)

        self.fire_cannons()

        for shell in self.shells:
            if shell.rect.left > 1600 or shell.rect.top > 900 or shell.rect.right < 0 or shell.rect.bottom < 0:
                self.shells.remove(shell)
            for plane in self.planes:
                if shell.rect.colliderect(plane.rect) and plane.active:
                    plane.take_damage()
                    self.enemy_hp += -1
                    self.shells.remove(shell)

    def fire_cannons(self):
        if self.firing:
            shots_fired = False
            for cannon in self.cannons:
                shot = cannon.fire()
                if shot is not None:
                    if self.current_ammo > 0:
                        shots_fired = True
                        self.shells.append(shot)
            if shots_fired:
                self.current_ammo += -1

    def start_reload(self):
        self.current_ammo = 0
        if not self.reloading:
            self.reload_left = self.reload_time
            self.reloading = True
        self.to_reload = False

    def reload(self):
        if self.reloading:
            if self.reload_left <= 0:
                self.reload_left = 0
                self.current_ammo = 4
                self.reloading = False
            else:
                self.reload_left += -1

    def display_ammo(self):
        text = pygame.font.Font(None, 30) \
            .render(str(self.current_ammo) + "/" + str(self.cannon_ammo), True, (220, 10, 10))
        self.screen.blit(text, (pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1] - 20))

        text = pygame.font.Font(None, 20) \
            .render(str(round(self.reload_left / 60, 1)), True, (220, 10, 10))
        self.screen.blit(text, (pygame.mouse.get_pos()[0] + 20, pygame.mouse.get_pos()[1] + 20))

    def spawn_plane(self):
        self.spawn_ticker += -1
        if self.spawn_ticker <= 0:
            try:
                current_plane = self.planes_iterator.__next__()
            except StopIteration:
                try:
                    self.planes_iterator = iter(self.planes)
                    current_plane = self.planes_iterator.__next__()
                except StopIteration:
                    current_plane = entities.Plane(self.screen, 0, 0)
                    current_plane.ready = False
            if current_plane.ready:
                current_plane.active = True
                self.spawn_ticker = 60 + random.randint(0, 120)
