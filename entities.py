import math
import random
from abc import ABC
from typing import Any

import pygame.sprite


class Entity(ABC, pygame.sprite.Sprite):

    def __init__(self, screen, x_position, y_position):
        super().__init__()
        self._x_size = 50
        self._y_size = 50
        self.set_image(x_position, y_position)
        self.screen = screen

    def set_image(self, x_position, y_position):
        self.image = pygame.Surface((self._x_size, self._y_size))
        self.image.fill([30, 30, 30])
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def update(self, *args: Any, **kwargs: Any) -> None:
        pygame.sprite.RenderPlain(self).draw(self.screen)


class MovingEntity(Entity, ABC):

    def __init__(self, screen, x_position, y_position):
        super().__init__(screen, x_position, y_position)
        self.x_speed = 0
        self.y_speed = 0

    def update(self, *args: Any, **kwargs: Any) -> None:
        super(MovingEntity, self).update()
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


class Plane(MovingEntity):
    base_image = pygame.image.load("sprites/Wing.png")
    image_damaged_1 = pygame.image.load("sprites/Wing damaged 1.png")
    image_damaged_2 = pygame.image.load("sprites/Wing damaged 2.png")
    image_damaged_3 = pygame.image.load("sprites/Wing damaged 3.png")

    def __init__(self, screen, x_position, y_position):
        super().__init__(screen, x_position, y_position)
        self.y_speed = 3
        self.hp = 4
        self.set_image(x_position, y_position)
        self.active = False
        self.bombs_dropped = False
        self.ready = True
        self._bombing_run_counter = 0
        self.image_flipped = False

    def bombing_run(self) -> int:
        if not self.bombs_dropped:
            self.active = False
        else:
            self.active = True
        damage_done = 0
        if not self.bombs_dropped:
            damage_done = self.hp
            self.bombs_dropped = True
        elif self._bombing_run_counter >= 120:
            if not self.image_flipped:
                self.image = pygame.transform.flip(self.image, False, True)
                self.image_flipped = True
            self.y_speed = -5
            self.rect.x = random.randint(0, 1600 - self.rect.width)
        self._bombing_run_counter += 1
        return damage_done

    def rearm(self):
        self.active = False
        self.image = pygame.transform.flip(self.image, False, True)
        self.image_flipped = False
        self.y_speed = 4
        self.rect.x = random.randint(0, 1600 - self.rect.width)
        self.rect.y = 0
        self.bombs_dropped = False
        self._bombing_run_counter = 0
        self.ready = True

    def take_damage(self):
        self.hp += -1
        match self.hp:
            case 3:
                self.image = Plane.image_damaged_1.convert_alpha()
            case 2:
                self.image = Plane.image_damaged_2.convert_alpha()
            case 1:
                self.image = Plane.image_damaged_3.convert_alpha()
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def set_image(self, x_position, y_position):
        self.image = Plane.base_image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def update(self, *args: Any, **kwargs: Any) -> None:
        if self.active:
            super(Plane, self).update()


class Cannon(Entity):
    image = pygame.image.load("sprites/Autocannon.png")

    shell_speed = 20

    def __init__(self, screen, x_position, y_position):
        self.aim_angle = 0
        self.original_image = Cannon.image.convert_alpha()
        self.original_center = None
        self.firing_cd = 0
        super().__init__(screen, x_position, y_position)

    def set_image(self, x_position, y_position):
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
        self.original_center = self.rect.center

    def fire(self):
        if self.firing_cd == 0:
            self.firing_cd = 30
            spread = random.uniform(-0.05, 0.05)
            return Shell(self.screen, self.rect.centerx, self.rect.centery,
                         Cannon.shell_speed * math.cos(self.aim_angle + spread),
                         Cannon.shell_speed * math.sin(self.aim_angle + spread))
        else:
            return None

    def update(self, *args: Any, **kwargs: Any) -> None:
        super(Cannon, self).update()
        if self.firing_cd > 0:
            self.firing_cd += -1
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos == (0, 0):
            self.aim_angle = -math.pi / 2
        else:
            vector_x = mouse_pos[0] - self.rect.centerx
            vector_y = mouse_pos[1] - self.rect.centery
            self.aim_angle = math.atan2(vector_y, vector_x)
        self.image = pygame.transform.rotate(self.original_image, (180 / math.pi) * -self.aim_angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.original_center


class Shell(MovingEntity):
    def __init__(self, screen, x_position, y_position, x_speed, y_speed):
        super().__init__(screen, x_position, y_position)
        self._x_size = 15
        self._y_size = 15
        self.set_image(x_position, y_position)
        self.x_speed = x_speed
        self.y_speed = y_speed

    def set_image(self, x_position, y_position):
        self.image = pygame.Surface((self._x_size, self._y_size), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position

    def update(self, *args: Any, **kwargs: Any) -> None:
        super(Shell, self).update()
        pygame.draw.circle(self.screen, (200, 0, 0), self.rect.center, self.rect.width / 2)
