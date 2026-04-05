from enum import IntEnum

class State(IntEnum):
    SPLASH = 1
    INSTRUCTION = 2
    PLAYING = 3
    LOST = 4
    WIN = 5
    PAUSE = 6

class GameMode(IntEnum):
    EASY = 1
    NORMAL = 2
    HARD = 3

