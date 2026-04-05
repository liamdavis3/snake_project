import random
from pyray import *
from os.path import join
from settings import * 
from anim import *
from enums import *


class Shot:
    def __init__(self, position: Vector2, velocity: int):
        self.position = Vector2(
            position.x * TILE_WIDTH + X_OFFSET + (TILE_WIDTH / 2),
            position.y * TILE_WIDTH + Y_OFFSET + (TILE_WIDTH / 2)
        )
        self.velocity = velocity
        self.alive = True

    def update(self, dt):
        self.position.x += self.velocity * dt

        if (self.position.x < X_OFFSET or self.position.x > X_OFFSET + TILES_WIDE*TILE_WIDTH):
            self.alive = False

    def draw(self):
        draw_circle(int(self.position.x), int(self.position.y), 10, GREEN)
        draw_circle(int(self.position.x), int(self.position.y), 7, DARKGREEN)