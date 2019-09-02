from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Snake:
    def __init__(self, pixel_size_coords, size):
        self.pos = [pixel_size_coords]
        self.direction = Direction.RIGHT
        self.need_new_tail = False
    def get_screen_coords(self, pixel_size):
        return [[coords[0] * pixel_size, coords[1] * pixel_size] for coords in self.pos]
    def get_head_screen_coords(self, pixel_size):
        return [self.pos[0][0] * pixel_size, self.pos[0][1] * pixel_size]
    def move(self):
        if self.direction == Direction.RIGHT:
            new_head = self.pos[0][0] + 1, self.pos[0][1]
        if self.direction == Direction.LEFT:
            new_head = (self.pos[0][0] - 1, self.pos[0][1])
        if self.direction == Direction.UP:
            new_head = (self.pos[0][0], self.pos[0][1] - 1)
        if self.direction == Direction.DOWN:
            new_head = (self.pos[0][0], self.pos[0][1] + 1)
        if self.need_new_tail:
            self.pos = [new_head] + self.pos
            self.need_new_tail = False
        else:
            self.pos = [new_head] + self.pos[:-1]
    def self_collision(self):
        if self.pos[0] in self.pos[1:]:
            print('self collision')
            return True
        return False
    def change_direction(self, direction):
        self.direction = direction
    def add_tail(self):
        self.need_new_tail = True
        
class Display:
    def __init__(self, width, height, pixel_size):
        self.scoreboard_height = 80
        self.border_width = 10
        self.inner_width = width
        self.inner_height = height
        self.pixel_size = pixel_size
        self.display = pygame.display.set_mode(self.get_window_size())
        self.background_color = black
        self.border_color = red
        self.font = pygame.font.Font('./Pixeled.ttf', 50)
        self.game_over_surface = self.font.render('GAME OVER', False, white)
        self.pause_surface = self.font.render('PAUSE', False, white)
    def clean_scoreboard(self):
        pygame.draw.rect(self.display, self.border_color, [self.border_width, 0] + [self.inner_width, self.scoreboard_height])
    def get_window_size(self):
        return [self.inner_width + 2 * self.border_width, self.inner_height + self.scoreboard_height + self.border_width]
    def get_playfield_size(self):
        return [self.inner_width, self.inner_height]
    def get_left_playfield_border(self):
        return self.border_width
    def get_right_playfield_border(self):
        return self.inner_width + self.border_width
    def get_upper_playfield_border(self):
        return self.scoreboard_height
    def get_lower_playfield_border(self):
        return self.scoreboard_height + self.inner_height
    def get_center(self):
        return [self.inner_width / 2, self.inner_height / 2]
    def update(self, snake, papu_coords, game_over, pause, points):
        if game_over:
            text_surface = self.game_over_surface
        elif pause:
            text_surface = self.pause_surface
        else:
            self.display.fill(self.border_color)
            pygame.draw.rect(self.display, self.background_color, [self.border_width, self.scoreboard_height] + self.get_playfield_size())
            snake_rects = [coords + [self.pixel_size, self.pixel_size] for coords in snake.get_screen_coords(self.pixel_size)]            
            for pixel in snake_rects:
                pygame.draw.rect(self.display, white, pixel)
            pygame.draw.rect(self.display, red, papu_coords + [self.pixel_size, self.pixel_size])
            text_surface = self.font.render(str(points), False, white)
        self.clean_scoreboard()
        self.display.blit(text_surface, (10, -40))
        pygame.display.update()
    def check_edge_collision(self, snake): #warunki bleh (nieczytelne) #move to game
        if snake.get_head_screen_coords(self.pixel_size)[0] < self.get_left_playfield_border():
            print('left edge collision')
            return True
        if snake.get_head_screen_coords(self.pixel_size)[0] + self.pixel_size > self.get_right_playfield_border():
            print('right edge collision')
            return True
        if snake.get_head_screen_coords(self.pixel_size)[1] + self.pixel_size > self.get_lower_playfield_border():    
            print('bottom edge collision')
            return True
        if snake.get_head_screen_coords(self.pixel_size)[1] < self.get_upper_playfield_border():
            print('top edge collision')
            return True
        return False

class Game:
    def __init__(self, board_size, pixel_size, delay):
        self.disp = Display(board_size, board_size, pixel_size)
        self.snake = Snake([self.disp.get_center()[0] / pixel_size, self.disp.get_center()[1] / pixel_size], pixel_size)
        self.clock = pygame.time.Clock()
        self.delay = delay
        self.game_over = False
        self.point_count = 0
        self.papu = [300.0,300.0]
        self.board_size = board_size
        self.scoreboard_height = 70 #to samo w display
        self.border_width = 10 #to samo w display
        self.inner_width = board_size #to samo w display
        self.inner_height = board_size #to samo w display
        self.left_boundry = self.border_width
        self.right_boundry = self.border_width + self.inner_width
        self.upper_boundry = self.scoreboard_height
        self.lower_boundry = self.scoreboard_height + self.inner_height
        self.pause = False
        self.pause_locked = True
        self.pixel_size = pixel_size
    def start(self):
        while not self.game_over:
            pygame.time.delay(self.delay)
            self.clock.tick()
            self.handle_events()
            if not self.pause:
                self.snake.move()
            self.game_over = self.check_collision()
            self.disp.update(self.snake, list(self.papu), self.game_over, self.pause, self.point_count)
        print('GAME OVER')   
        print('POINTS: ', self.point_count)
    def check_collision(self): #moze apply_move_effects (i wpisywac dane ze kolizja albo ze zjadlo jedzonko)
        if self.disp.check_edge_collision(self.snake):
            return True
        if self.snake.self_collision():
            return True
        if self.check_papu_collision(): #SIDE EFFECT?
            self.snake.add_tail()
            self.point_count += 1
        return False
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        self.handle_keys_pressed(keys)
    def handle_keys_pressed(self, keys):
        if keys[pygame.K_LEFT]:
            self.snake.change_direction(Direction.LEFT)
        if keys[pygame.K_RIGHT]:
            self.snake.change_direction(Direction.RIGHT)
        if keys[pygame.K_UP]:
            self.snake.change_direction(Direction.UP)
        if keys[pygame.K_DOWN]:
            self.snake.change_direction(Direction.DOWN)
        if keys[pygame.K_p]:
            self.toggle_pause()
        else:
            self.lock_pause()
    def toggle_pause(self):
        if self.pause == True and self.pause_locked:
            self.pause = False
            self.pause_locked = False
        elif self.pause == False and self.pause_locked:
            self.pause = True
            self.pause_locked = False
    def lock_pause(self):
        self.pause_locked = True
    #PODEBRANE Z BOARD, DO POPRAWKI
    def check_papu_collision(self):
        print('checking papu collision')
        print('papu: ', self.papu)
        print('head: ', self.snake.get_head_screen_coords(self.pixel_size))
        if self.papu == self.snake.get_head_screen_coords(self.pixel_size):
            self.new_papu(self.snake)
            return True
        return False
    def new_papu(self, snake):
        num_of_pixels_width = self.board_size / pixel_size
        num_of_pixels_height = self.board_size / pixel_size
        new_papu_coords = [self.left_boundry + random.randint(0, num_of_pixels_width - 1) * pixel_size, self.upper_boundry + random.randint(0, num_of_pixels_height - 1) * pixel_size]
        if snake is not None and new_papu_coords in snake.get_screen_coords(self.pixel_size):
            new_papu(self, snake)
        else:
            self.papu = new_papu_coords #moze zamiast w funkcji przypisywac funkcja powinna zwracac?

class Button:
    def __init__(self):
        pass

#-------------------------------------------------------------------------------------

import pygame
import random


pygame.init()
from pygame.locals import *


black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)

board_size = 560
pixel_size = 10

time_delay = 50


game = Game(board_size, pixel_size, time_delay)

game.start()

pygame.time.delay(500)
