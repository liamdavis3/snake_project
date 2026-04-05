from pyray import *
from settings import *

from enum import IntEnum

# Warm-up difference with class code: couple of addition and fixes
# have been done

# This demo is using a different sheet; and has a own main to demo
# provided capability of class Animation
# It is just a proof of concept of the code we study in class

# Main task: Integrate with your own main.py, class Game/Player

# Your class Game and Player should use clean update function
# based on a planned state machine diagram of the action (state/transition)
# player can undergo

class AnimationType(IntEnum):
    REPEATING = 1
    ONESHOT = 2

class Direction(IntEnum):
    LEFT = -1
    RIGHT = 1

class Animation:
    def __init__(self, first, last, cur, step, duration, duration_left, anim_type, row, sprites_in_row):
        self.first = first
        self.last = last
        self.cur = cur
        self.step = step
        self.duration = duration
        self.duration_left = duration_left
        self.type = anim_type
        self.row = row
        self.sprites_in_row = sprites_in_row 
        self.done = False
        self.direction = Direction.RIGHT
        self.directions = [Direction.RIGHT, Direction.LEFT]
        self.frame_rec = Rectangle(0,0, SPRITE_SHEET_TILE_WIDTH, SPRITE_SHEET_TILE_HEIGHT)

    def update(self, dt):
        self.duration_left -= dt
        
        if (self.duration_left<=0):
            self.duration_left = self.duration
            self.cur += self.step

            if (self.cur > self.last):
                match(self.type):
                    case AnimationType.ONESHOT:
                        self.cur = self.last 
                        self.done = True
                    case AnimationType.REPEATING:
                        self.cur = self.first 

    def frame(self, row):  # FIXES happened there to generalize to sprite sheet
        self.frame_rec.x = (self.cur % self.sprites_in_row) * SPRITE_SHEET_TILE_WIDTH
        self.frame_rec.y = SPRITE_SHEET_TILE_HEIGHT * self.row
        self.frame_rec.width = SPRITE_SHEET_TILE_WIDTH
        return self.frame_rec

    def reset(self): # ADDED
        self.cur = self.first
        self.done = False
        self.type = AnimationType.REPEATING
