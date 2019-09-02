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
            new_head = self.pos[0][:] #without [:] would assign reference to list, not it's copy
            new_head[0] += 1
        if self.direction == Direction.LEFT:
            new_head = self.pos[0][:]
            new_head[0] -= 1
        if self.direction == Direction.DOWN:
            new_head = self.pos[0][:]
            new_head[1] += 1
        if self.direction == Direction.UP:
            new_head = self.pos[0][:]
            new_head[1] -= 1
        if self.need_new_tail:
            self.pos = [new_head] + self.pos
            self.need_new_tail = False
        else:
            self.pos = [new_head] + self.pos[:-1]
    def if_self_collision(self): #not sure about the name
        if self.pos[0] in self.pos[1:]:
            print('self collision')
            return True
        return False
    def change_direction(self, direction):
        #check if valid value
        if self.direction == Direction.LEFT and direction == Direction.RIGHT:
            return
        if self.direction == Direction.RIGHT and direction == Direction.LEFT:
            return
        if self.direction == Direction.UP and direction == Direction.DOWN:
            return
        if self.direction == Direction.DOWN and direction == Direction.UP:
            return
        self.direction = direction
    def add_tail(self):
        self.need_new_tail = True
        
class Display:
    def __init__(self, width, height, border_width, pixel_size, colors):
        self.scoreboard_height = 80
        self.inner_width = width
        self.inner_height = height
        self.pixel_size = pixel_size
        self.border_width = border_width
        self.background_color = colors[0]
        self.border_color = colors[1]
        self.display = pygame.display.set_mode(self.get_window_size())
        self.font = pygame.font.Font('./Pixeled.ttf', 50)
        self.game_over_surface = self.font.render('GAME OVER', False, white)
        self.pause_surface = self.font.render('PAUSE', False, white)
    def clean_scoreboard(self):
        pygame.draw.rect(self.display, self.border_color, [self.border_width, 0] + [self.inner_width, self.scoreboard_height])
    def get_window_size(self):
        return [self.inner_width + 2 * self.border_width, self.inner_height + self.scoreboard_height + self.border_width]
    def get_playfield_size(self):
        return [self.inner_width, self.inner_height]
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
            pygame.draw.rect(self.display, (0,0,255), papu_coords + [self.pixel_size, self.pixel_size])
            text_surface = self.font.render(str(points), False, white)
        self.clean_scoreboard()
        self.display.blit(text_surface, (self.border_width, -40))
        pygame.display.update()
    def move_x_to_inner_field(self, x_coord):
        return x_coord + self.border_width
    def move_y_to_inner_field(self, y_coord):
        return y_coord + self.scoreboard_height
    def move_to_inner_field(self, coords):
        return [move_x_to_inner_field(coords[0]), move_y_to_inner_field(coords[1])]
    
class Game:
    def __init__(self, board_size, pixel_size, delay):
        self.disp = Display(board_size, board_size, pixel_size, pixel_size, [black, red])
        self.snake = Snake([self.disp.get_center()[0] / pixel_size, self.disp.get_center()[1] / pixel_size], pixel_size)
        self.clock = pygame.time.Clock()
        self.delay = delay
        self.game_over = False
        self.point_count = 0
        self.papu = [300.0,300.0]
        self.board_size = board_size
        self.inner_width = board_size #to samo w display
        self.inner_height = board_size #to samo w display
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
                self.apply_move_effcts()
            self.disp.update(self.snake, list(self.papu), self.game_over, self.pause, self.point_count)
        print('GAME OVER')   
        print('POINTS: ', self.point_count)
    def apply_move_effcts(self):
        if self.if_edge_collision() or self.snake.if_self_collision():
            self.game_over = True
        elif self.if_papu_eaten():
            self.snake.add_tail()
            self.point_count += 1
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
    def if_papu_eaten(self):
        if self.papu == self.snake.get_head_screen_coords(self.pixel_size):
            print('papu eaten')
            self.new_papu(self.snake)
            return True
        return False
    def new_papu(self, snake):
        num_of_pixels_width = self.board_size / pixel_size
        num_of_pixels_height = self.board_size / pixel_size
        new_papu_coords = [self.disp.move_x_to_inner_field(0) + random.randint(0, num_of_pixels_width - 1) * pixel_size, self.disp.move_y_to_inner_field(0) + random.randint(0, num_of_pixels_height - 1) * pixel_size]
        if snake is not None and new_papu_coords in snake.get_screen_coords(self.pixel_size):
            self.new_papu(snake)
        else:
            self.papu = new_papu_coords #moze zamiast w funkcji przypisywac funkcja powinna zwracac?
        print('papu: ', self.papu)
    def if_edge_collision(self): #not sure about the name
        snake_head_left_x, snake_head_top_y = self.snake.get_head_screen_coords(self.pixel_size)
        snake_head_right_x = snake_head_left_x + self.pixel_size
        snake_head_bottom_y = snake_head_top_y + self.pixel_size
        if snake_head_left_x < self.disp.move_x_to_inner_field(0):
            print('left edge collision')
            return True
        if snake_head_right_x > self.disp.move_x_to_inner_field(self.inner_width):
            print('right edge collision')
            return True
        if snake_head_top_y < self.disp.move_y_to_inner_field(0):
            print('top edge collision')
            return True
        if snake_head_bottom_y > self.disp.move_y_to_inner_field(self.inner_height):    
            print('bottom edge collision')
            return True
        return False


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

board_size = 500
pixel_size = 10

time_delay = 50


game = Game(board_size, pixel_size, time_delay)

game.start()

pygame.time.delay(500)
