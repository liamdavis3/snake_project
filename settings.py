from pyray import *
from raylib import *
from random import randint, uniform
from os.path import join


FPS = 120
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TILES_WIDE, TILES_TALL = 20, 14
TILE_WIDTH = 35
X_OFFSET = 50
Y_OFFSET = 100

SPRITE_SHEET_TILE_WIDTH = 24
SPRITE_SHEET_TILE_HEIGHT = 32

SNAKE_SPEED_NORMAL = FPS//10
SNAKE_SPEED_SLOW = FPS//8


MOVE_UP = Vector2(0,-1)
MOVE_LEFT = Vector2(-1,0)
MOVE_DOWN = Vector2(0,1)
MOVE_RIGHT = Vector2(1,0)

LIGHTGRAY_TRANSPARENT = Color(200, 200, 200, 80)



