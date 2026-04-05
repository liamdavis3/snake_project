import random
from pyray import *
from os.path import join
from settings import * 
from anim import *
from game import *
from snake import *
from enums import *
from shot import *



class Apple:
    def __init__(self, mode: GameMode):
        self.position = Vector2(randint(1,TILES_WIDE-1), randint(1,TILES_TALL-1))
        self.size = Vector2(TILE_WIDTH,TILE_WIDTH)
        self.color = RED
        self.eaten = False
        self.mode = mode
        self.can_shoot = True     
        

    def startup(self):
        self.texture = load_texture(join('assets', 'harry_sprite.png'))

        self.dest = Rectangle(0, 0, TILE_WIDTH, TILE_WIDTH)
        self.origin = Vector2(0, 0)
        self.animation = Animation(
            first=0, 
            last=4, 
            cur=0,
            step=1, 
            duration=0.2, 
            duration_left=0.1,
            anim_type=AnimationType.REPEATING,
            row=1, 
            sprites_in_row=5,
        )
        self.animation_attack = Animation(
            first=0, 
            last=8, 
            cur=0,
            step=1, 
            duration=0.2, 
            duration_left=0.1,
            anim_type=AnimationType.REPEATING,
            row=0, 
            sprites_in_row=9,
        )

    def update(self, snake: Snake, dt: float):
        
        if self.eaten == True: 
            self.position = self.find_spawn(snake)
            self.eaten = False

        match self.mode:
            case GameMode.EASY | GameMode.NORMAL:
                Animation.update(self.animation, dt)
            case GameMode.HARD:
                Animation.update(self.animation_attack, dt)
                if self.animation_attack.cur == self.animation_attack.last and self.can_shoot:
                    self.can_shoot = False
                    return Vector2(self.position.x, self.position.y), Vector2(self.animation.direction, 0)
                
                if self.animation_attack.cur == 0:
                    self.can_shoot = True

    def find_spawn(self, snake: Snake):
        while True:
            x = randint(0,TILES_WIDE-1)
            y = randint(0,TILES_TALL-1)
            good = True
            for part in snake.body:
                if x == part.position.x and y == part.position.y:
                    good = False
                    break
            if good:
                self.animation.direction = random.choice(self.animation.directions)
                self.animation.cur = 0
                self.animation_attack.cur = 0
                return Vector2(x,y)

    def draw(self):

        match self.mode:
            case GameMode.EASY | GameMode.NORMAL:
                player_frame = Animation.frame(self.animation, self.animation.row)
                self.dest.x = int(self.position.x*TILE_WIDTH+X_OFFSET)
                self.dest.y = int(self.position.y*TILE_WIDTH+Y_OFFSET)
                player_frame.width *= self.animation.direction
                draw_texture_pro(
                    self.texture,
                    player_frame,
                    self.dest,
                    self.origin, 0.0, WHITE,
                )
            case GameMode.HARD:
                player_frame = Animation.frame(self.animation_attack, self.animation_attack.row)
                self.dest.x = int(self.position.x*TILE_WIDTH+X_OFFSET)
                self.dest.y = int(self.position.y*TILE_WIDTH+Y_OFFSET)
                player_frame.width *= self.animation.direction
                draw_texture_pro(
                    self.texture,
                    player_frame,
                    self.dest,
                    self.origin, 0.0, WHITE,
                )

    def shutdown(self):
        unload_texture(self.texture)