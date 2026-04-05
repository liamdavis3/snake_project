import random
from pyray import *
from os.path import join
from settings import * 
from enum import IntEnum
from enums import *
from anim import *
from apple import Apple
from snake import Snake
from segment import Segment
from shot import *


class Game:
    def __init__(self):
        init_audio_device()
        self.mode = GameMode.NORMAL
        self.state = State.SPLASH
        self.snake = Snake()
        self.apple = Apple(self.mode)
        self.shots = []
        
        self.frame_count = 0
        self.speed = SNAKE_SPEED_NORMAL
        self.dev = False
        self.high_score = 0
        self.all_time_high_score = self.load_high_score()
        
    def startup(self):
        self.apple.startup()
        self.snake.startup()
        self.splash_texture = load_texture(join('assets', 'SPLASH.png'))
        self.instruction_texture = load_texture(join('assets', 'instruction_SPLASH.png'))
        self.lost_texture = load_texture(join('assets', 'end_SPLASH.png'))
        self.win_texture = load_texture(join('assets', 'win_SPLASH.png'))
        self.play_background = load_texture(join('assets', 'playing_background_new.png'))
        self.music = load_music_stream(join('assets', 'garden_song.mp3'))
        play_music_stream(self.music)

        self.difficulty_map = {
            GameMode.EASY : (16, KEY_ONE, "Easy", (313,355,35,35)),
            GameMode.NORMAL : (12, KEY_TWO, "Normal", (313,390,35,35)),
            GameMode.HARD : (12, KEY_THREE, "Hard", (313,425,35,35))
        }

    def reset(self, score: int):
        if score > self.high_score:
            self.high_score = score        
        if score > self.all_time_high_score:
            self.write_high_score(score)
            self.all_time_high_score = score
            
        self.speed = SNAKE_SPEED_NORMAL
        self.snake = Snake()
        self.snake.speed = self.speed
        self.apple = Apple(self.mode)
        self.frame_count = 0
        self.apple.startup()
        self.snake.startup()
        self.shots.clear()
        self.state = State.SPLASH

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except:
            return 0

    def write_high_score(self, score: int):
        with open("highscore.txt", "w") as file:
            file.write(str(score))

#----------------Update helper functions--------------------

    def check_shot(self, shot: Shot):
        if shot:
            self.shots.append(shot)

    def check_press_enter(self, go_to_state: State):
        if is_key_pressed(KEY_ENTER):
            self.state = go_to_state
            return True

    def update_dev_analytics(self):
        if is_key_pressed(KEY_G):
            self.snake.body.append(Segment(self.snake.body[-1].position, self.snake.body[-1].direction))

    def get_playing_mode_input(self):
        for mode, (speed, key, name, position) in self.difficulty_map.items():
            if is_key_pressed(key):
                self.speed = speed
                self.snake.speed = speed
                self.mode = mode
                self.apple.mode = mode

    def update_snake(self):
        if not self.snake.alive:
            self.state = State.LOST
        if len(self.snake.body) == 278:
            self.state = State.WIN
        self.snake.update()
        self.frame_count += 1
        if self.frame_count % self.speed == 0 and self.snake.alive == True:
            self.snake.move(self.apple)

    def update_apple_and_shots(self, dt):
        shot_result = self.apple.update(self.snake, dt)
        if shot_result:
            position, direction = shot_result
            velocity = randint(200,350)
            position.x += -direction.x
            self.shots.append(Shot(position, -direction.x*velocity))
        self.check_shot_snake_collision(dt)

    def check_shot_snake_collision(self, dt: float):
        bad_shots = []
        for shot in self.shots:
            if not shot.alive:
                bad_shots.append(shot)
                continue
            shot.update(dt)
            rect = Rectangle(0,0,TILE_WIDTH,TILE_WIDTH)
            self.snake_ball_collision_formula(shot, bad_shots, rect)
        self.clear_bad_shots(bad_shots)
    
    def snake_ball_collision_formula(self, shot: Shot, bad_shots: list, rect: Rectangle):
        for i, segment in enumerate(self.snake.body):
                rect.x = segment.position.x * TILE_WIDTH + X_OFFSET
                rect.y = segment.position.y * TILE_WIDTH + Y_OFFSET
                if check_collision_circle_rec(shot.position, 10, rect):
                    shot.alive = False
                    bad_shots.append(shot)
                    if i == 0:
                        self.snake.remove_tail(5)
                        break
                    else:
                        self.snake.remove_tail(1)
                        break

    def clear_bad_shots(self, bad_shots: list):
        for shot in bad_shots:
            self.shots.remove(shot)

    def manual_adjust_speed(self):
        if is_key_pressed(KEY_COMMA):
            self.speed -= 1
            self.snake.speed -=1
        if is_key_pressed(KEY_PERIOD):
            self.speed += 1
            self.snake.speed +=1


#----------------drawing helper functions-----------------
    @staticmethod
    def draw_guards():
        for i in range(TILES_WIDE + 1):
            x = TILE_WIDTH * i + X_OFFSET
            draw_line(x, Y_OFFSET, x, Y_OFFSET + TILES_TALL * TILE_WIDTH, LIGHTGRAY_TRANSPARENT)
        for i in range(TILES_TALL + 1):
            y = TILE_WIDTH * i + Y_OFFSET
            draw_line(X_OFFSET, y, X_OFFSET + TILES_WIDE * TILE_WIDTH, y, LIGHTGRAY_TRANSPARENT)

    def draw_scores(self):
        draw_text(f"Score: {self.snake.score}", 50, 60, 30, LIGHTGRAY)
        draw_text(f"High Score: {self.high_score}", 220, 60, 30, LIGHTGRAY)
        draw_text(f"All Time Score: {self.all_time_high_score}", 470, 60, 30, LIGHTGRAY)

    def draw_shots(self):
        for shot in self.shots:
            if shot.alive:
                shot.draw()
    

    def draw_dev_mode(self):
        draw_rectangle(X_OFFSET, Y_OFFSET+TILE_WIDTH*9, TILE_WIDTH*8,TILE_WIDTH*5, Color(BLUE[0],BLUE[1],BLUE[2],150))
        draw_text(f"Press G to grow", X_OFFSET + 5, Y_OFFSET+TILE_WIDTH*9+10, 25, LIGHTGRAY)
        draw_text(f"Speed: {self.snake.speed}", X_OFFSET + 5,Y_OFFSET+TILE_WIDTH*10, 20, LIGHTGRAY)
        draw_text(f"Speed: {self.snake.speed}", X_OFFSET + 5 ,Y_OFFSET+TILE_WIDTH*10, 20, LIGHTGRAY)
        draw_text(f"LERP: {self.snake.speed}", X_OFFSET +5,Y_OFFSET+TILE_WIDTH*10+25, 20, LIGHTGRAY)
        draw_text(f"t: {(self.frame_count % self.speed) / self.speed:.2f}",X_OFFSET+5, Y_OFFSET+TILE_WIDTH*10+50, 20, LIGHTGRAY)
        draw_text(f"Lerp X: {self.snake.lerp_vector.x:.2f} Y: {self.snake.lerp_vector.y:.2f}", X_OFFSET+5, Y_OFFSET+TILE_WIDTH*10+75, 20, LIGHTGRAY)
        for segment in self.snake.body:
            x = int(segment.position.x * TILE_WIDTH + X_OFFSET)
            y = int(segment.position.y * TILE_WIDTH + Y_OFFSET)
            draw_rectangle_lines(x, y, TILE_WIDTH, TILE_WIDTH, GREEN)
        draw_rectangle_lines(int(self.apple.position.x * TILE_WIDTH + X_OFFSET), int(self.apple.position.y * TILE_WIDTH + Y_OFFSET), TILE_WIDTH, TILE_WIDTH, RED)
        for shot in self.shots:
            x = int(shot.position.x)
            y = int(shot.position.y)
            draw_circle_lines(x, y, 11, RED)
        for i, part in enumerate(self.snake.body):
            x = int(part.position.x * TILE_WIDTH + X_OFFSET)
            y = int(part.position.y * TILE_WIDTH + Y_OFFSET)
            draw_text(str(i), x+5, y+5, 10, PINK)
        draw_text(f"{get_frame_time()*1000:.2f} ms", X_OFFSET+5, Y_OFFSET+TILE_WIDTH*10+100, 20, LIGHTGRAY)


#----------main loop functions-------------
    def update(self):
        update_music_stream(self.music)
        dt = get_frame_time()

        match self.state:
            case State.SPLASH:
                self.check_press_enter(State.INSTRUCTION)
            case State.INSTRUCTION:
                self.check_press_enter(State.PLAYING)
                self.get_playing_mode_input()
            case State.PLAYING:
                self.update_snake()
                self.update_apple_and_shots(dt)
                self.manual_adjust_speed()
                if is_key_pressed(KEY_P) or is_key_pressed(KEY_SPACE):
                    self.state = State.PAUSE
            case State.WIN:
                if self.check_press_enter(State.SPLASH):
                    self.reset(self.snake.score)
            case State.LOST:
                if self.check_press_enter(State.SPLASH):
                    self.reset(self.snake.score)
            case State.PAUSE:
                self.manual_adjust_speed()
                if is_key_pressed(KEY_P) or is_key_pressed(KEY_SPACE):
                    self.state = State.PLAYING

        if is_key_pressed(KEY_I):
            self.dev = not self.dev
        self.update_dev_analytics()

    def draw(self):
        match self.state:
            case State.SPLASH:
                draw_texture(self.splash_texture, 0, 0, WHITE)
            case State.INSTRUCTION:
                draw_texture(self.instruction_texture, 0, 0, WHITE)
                speed, key, name, position = self.difficulty_map.get(self.mode)
                draw_rectangle_lines(position[0],position[1],position[2],position[3],PINK)
            case State.WIN:
                draw_texture(self.win_texture, 0, 0, WHITE)
            case State.LOST:
                draw_texture(self.lost_texture, 0, 0, WHITE)
            case State.PLAYING:
                clear_background(LIGHTGRAY)
                draw_texture(self.lost_texture, 0, 0, DARKGRAY)
                draw_texture(self.play_background,X_OFFSET,Y_OFFSET, LIGHTGRAY)
                self.draw_guards()
                self.draw_scores()
                self.snake.draw((self.frame_count % self.speed) / self.speed)
                self.apple.draw()
                self.draw_shots()
                if self.dev:
                    self.draw_dev_mode()
            case State.PAUSE:
                clear_background(LIGHTGRAY)
                draw_texture(self.lost_texture, 0, 0, DARKGRAY)
                draw_texture(self.play_background,X_OFFSET,Y_OFFSET, LIGHTGRAY)
                self.draw_guards()
                self.draw_scores()
                self.snake.draw((self.frame_count % self.speed) / self.speed)
                self.apple.draw()
                self.draw_shots()
                if self.dev:
                    self.draw_dev_mode()
                draw_text("Paused", 350,350,30, Color(RED[0],RED[1],RED[2],200))
        draw_fps(20, 20)

    def shutdown(self):
       self.apple.shutdown()
       self.snake.shutdown()
       unload_texture(self.play_background)
       unload_texture(self.splash_texture)
       unload_texture(self.lost_texture)
       unload_texture(self.instruction_texture)
       unload_texture(self.win_texture)
       unload_music_stream(self.music)
       close_audio_device()
