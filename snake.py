from pyray import *
from os.path import join
from settings import * 
from collections import deque
from apple import *
from game import *
from segment import *
from enums import *

class Snake:
    def __init__(self):
        self.body = deque()
        self.body.appendleft(Segment(Vector2(0,0), Vector2(0,0)))
        self.prev_body = deque(maxlen=2)
        self.direction_queue = deque()  
        self.new_head = Vector2(0,0)
        self.direction = Vector2(0,0)
        self.next_direction = Vector2(0,0)
        self.lerp_vector = Vector2(0,0)

        self.speed = SNAKE_SPEED_NORMAL
        self.score = 0
        self.alive = True
        self.body_color = Color(49, 40, 231, 240)
        self.body_second_color = BLACK

    
    def startup(self):
       self.texture = load_texture(join('assets', 'head_blue.png'))
       self.bite_sound = load_sound(join('assets', 'break.mp3'))
       

       #head turning
       self.source_down = Rectangle(0,0, 35, 35)
       self.source_up = Rectangle(0,0, 35, -35)
       self.source_left_right = Rectangle(0,0, 35, 35)
       
       self.dest = Rectangle(0,0,TILE_WIDTH,TILE_WIDTH)
       self.origin_down  = Vector2(0, 0)
       self.origin_up    = Vector2(0, 0)
       self.origin_left  = Vector2(0, 35)
       self.origin_right = Vector2(35, 0)
       
       self.mini_offset_right = (0, 17.5)
       self.mini_offset_left = (35, 17.5)
       self.mini_offset_down = (17.5, 0)
       self.mini_offset_up = (17.5, 35)
       self.mini_offset_idle = (17.5, 17.5)   

       self.head_map = {
            (0,-1): (self.source_up, self.origin_up, 0, self.mini_offset_up),
            (-1,0): (self.source_left_right, self.origin_left, 90.0, self.mini_offset_left),
            (0, 1): (self.source_down, self.origin_down, 0, self.mini_offset_down),
            (1, 0): (self.source_left_right, self.origin_right, -90, self.mini_offset_right),
            (0, 0): (self.source_left_right, self.origin_right, -90, self.mini_offset_idle)
        }
       
       self.direction_key = (0,0)

    def update(self):

        if (is_key_pressed(KEY_UP) or is_key_pressed(KEY_W)): 
            self.direction_queue.append(MOVE_UP)
        if (is_key_pressed(KEY_LEFT) or is_key_pressed(KEY_A)): 
            self.direction_queue.append(MOVE_LEFT)
        if (is_key_pressed(KEY_DOWN) or is_key_pressed(KEY_S)): 
            self.direction_queue.append(MOVE_DOWN)
        if (is_key_pressed(KEY_RIGHT) or is_key_pressed(KEY_D)):
            self.direction_queue.append(MOVE_RIGHT)   
     
        
    def move(self, apple: Apple):

        #for lerp to not glitch
        self.prev_body = self.body.copy()

        if self.direction_queue:
            next_direction = self.direction_queue.popleft()
            if (next_direction.x != -self.direction.x or next_direction.y != -self.direction.y):
                self.direction = next_direction

        if (self.snake_wall_collide() or self.snake_self_collide()):
            self.alive = False
        else:
            self.new_head = vector2_add(self.body[0].position, self.direction)
    
        self.body.appendleft(Segment(self.new_head, self.direction))
        self.body.pop()
        self.check_apple_collision(apple)
        self.direction_key = (self.direction.x, self.direction.y)
        
    def lerp(self, v1, v2, t):
        #a + (b - a) * t
        self.lerp_vector.x = v1.position.x + (v2.position.x - v1.position.x) * t
        self.lerp_vector.y = v1.position.y + (v2.position.y - v1.position.y) * t


    def draw(self, t: float):
        
        for i, chunk in enumerate(self.body):
            #lerp prev alignment
            if i < len(self.prev_body):
                prev_chunk = self.prev_body[i]
            else:
                prev_chunk = chunk 
            self.lerp(prev_chunk,chunk,t)
            x = int(self.lerp_vector.x * TILE_WIDTH + X_OFFSET)
            y = int(self.lerp_vector.y * TILE_WIDTH + Y_OFFSET)

            source, origin, rotation, offset = self.head_map.get((chunk.direction.x, chunk.direction.y))
            if i == 0:
                self.draw_snake_head(x, y, source, origin, rotation, offset)
            else:
                self.draw_body_segment(x, y, offset)
               
                
    def draw_snake_head(self, x: int, y: int, source: Rectangle, origin: Rectangle, rotation: float, offset: tuple):
        self.dest.x = x
        self.dest.y = y
        self.draw_smaller_connection_body_part(x, y, offset)
        draw_texture_pro(
            self.texture,
            source,
            self.dest,
            origin,
            rotation,
            WHITE
        )
    
    def draw_body_segment(self, x: int, y: int, offset: tuple):
        self.draw_smaller_connection_body_part(x,y,offset)
        draw_circle(int(x + 17.5), int(y + 17.5), 14.5, self.body_color)
        draw_circle(int(x + 17.5), int(y + 17.5), 5, self.body_second_color)

    def draw_smaller_connection_body_part(self, x: int, y: int, offset: tuple):
        circle_x = x + offset[0]
        circle_y = y + offset[1]
        draw_circle(int(circle_x), int(circle_y), 8, self.body_color)
        draw_circle(int(circle_x), int(circle_y), 3, self.body_second_color)

    def snake_self_collide(self) -> bool:
        if(len(self.body) > 4):
            for body in list(self.body)[1:]:
                if self.new_head.x==body.position.x and self.new_head.y==body.position.y:
                    return True
        return False
    
    def snake_wall_collide(self) -> bool:
        if(self.new_head.x + self.direction.x > TILES_WIDE - 1
           or self.new_head.y + self.direction.y > TILES_TALL - 1
           or self.new_head.x + self.direction.x < 0
           or self.new_head.y + self.direction.y < 0):
            return True
        return False
    
    def check_apple_collision(self, apple: Apple):
        if(int(self.new_head.x) == int(apple.position.x) and 
           int(self.new_head.y) == int(apple.position.y)):
            apple.eaten = True
            play_sound(self.bite_sound)
            print("eat")
            self.body.append(Segment(self.body[-1].position, self.body[-1].direction))
            self.recent = self.body[-1]
            self.score += 1

    def remove_tail(self, remove):
        if len(self.body) == 1:
            self.alive = False
        for i in range(remove):
            if len(self.body) > 1:
                self.body.pop()
                self.score -=1
        

    def shutdown(self):
        unload_texture(self.texture)
        unload_sound(self.bite_sound)