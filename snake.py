from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

class Snake:
    def __init__(self, coords, size):
        self.pos = [coords]
        self.size = size
        self.direction = Direction.RIGHT
        self.need_new_tail = False
    def get_rects(self):
        rects_list = []
        for chunk in self.pos:
            rects_list.append(list(chunk) + [self.size, self.size])
        return rects_list
    def get_head_coords(self):
        return self.pos[0]
    def move(self):
        if self.direction == Direction.RIGHT:
            new_head = self.pos[0][0] + self.size, self.pos[0][1]
        if self.direction == Direction.LEFT:
            new_head = (self.pos[0][0] - self.size, self.pos[0][1])
        if self.direction == Direction.UP:
            new_head = (self.pos[0][0], self.pos[0][1] - self.size)
        if self.direction == Direction.DOWN:
            new_head = (self.pos[0][0], self.pos[0][1] + self.size)
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
    def game_over_detection():
        pass
        
class Display:
    def __init__(self, width, height, pixel_size):
        self.scoreboard_height = 70
        self.border_width = 10
        self.inner_width = width
        self.inner_height = height
        self.pixel_size = pixel_size
        self.display = pygame.display.set_mode(self.get_window_size())
        self.background_color = black
        self.border_color = red
        self.game_over = False
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
    def update(self, snake, papu_coords, pause, points):
        self.display.fill(self.border_color)
        pygame.draw.rect(self.display, self.background_color, [self.border_width, self.scoreboard_height] + self.get_playfield_size())
        for chunk in snake.get_rects():
            pygame.draw.rect(self.display, white, chunk)
        pygame.draw.rect(self.display, red, papu_coords + [self.pixel_size, self.pixel_size])
        if pause:
            for pixel in [[x, y, w, h] for [x, y, w, h] in self.get_pause_rects()]: #bleh
                pygame.draw.rect(self.display, white, pixel)
        if self.game_over:
            for pixel in [[x, y, w, h] for [x, y, w, h] in self.get_game_over_rects()]: #bleh
                pygame.draw.rect(self.display, white, pixel)
        myfont = pygame.font.Font('./Pixeled.ttf', 70)
        textsurface = myfont.render(str(points), False, (255, 255, 255))
        self.display.blit(textsurface,(0,0))
        pygame.display.update()
    def check_edge_collision(self, snake): #warunki bleh (nieczytelne) 
        if snake.get_head_coords()[0] < self.get_left_playfield_border():
            print('border hit! coords:' + str(snake.get_head_coords()))
            return True
        if snake.get_head_coords()[0] + self.pixel_size > self.get_right_playfield_border():
            print('border hit! coords:' + str(snake.get_head_coords()))
            return True
        if snake.get_head_coords()[1] + self.pixel_size > self.get_lower_playfield_border():    
            print('border hit! coords:' + str(snake.get_head_coords()))
            return True
        if snake.get_head_coords()[1] < self.get_upper_playfield_border():
            print('border hit! coords:' + str(snake.get_head_coords()))
            return True
        return False
    def get_pause_rects(self):
        pause_coords = [(1,1),(2,1),(3,1),    (6,1),(7,1),(8,1),    (11,1),       (13,1),    (16,1),(17,1),(18,1),    (21,1),(22,1),(23,1),
                        (1,2),      (3,2),    (6,2),      (8,2),    (11,2),       (13,2),    (16,2),                  (21,2),
                        (1,3),(2,3),(3,3),    (6,3),(7,3),(8,3),    (11,3),       (13,3),    (16,3),(17,3),(18,3),    (21,3),(22,3),
                        (1,4),                (6,4),      (8,4),    (11,4),       (13,4),                  (18,4),    (21,4),
                        (1,5),                (6,5),      (8,5),    (11,5),(12,5),(13,5),    (16,5),(17,5),(18,5),    (21,5),(22,5),(23,5)]
        pause_rects = [[x * 10, y * 10, self.pixel_size, self.pixel_size] for (x, y) in pause_coords]
        return pause_rects
    def get_game_over_rects(self):
        game_coords = [(1,1),(2,1),(3,1),(4,1),(5,1),    (8,1),(9,1),(10,1),(11,1),(12,1),    (15,1),                     (19,1),    (22,1),(23,1),(24,1),(25,1),(26,1),
                       (1,2),                            (8,2),                    (12,2),    (15,2),(16,2),       (18,2),(19,2),    (22,2),
                       (1,3),            (4,3),(5,3),    (8,3),(9,3),(10,3),(11,3),(12,3),    (15,3),       (17,3),       (19,3),    (22,3),(23,3),(24,3),(25,3),
                       (1,4),                  (5,4),    (8,4),                    (12,4),    (15,4),                     (19,4),    (22,4),
                       (1,5),(2,5),(3,5),(4,5),(5,5),    (8,5),                    (12,5),    (15,5),                     (19,5),    (22,5),(23,5),(24,5),(25,5),(26,5)]

        over_coords = [(1,1),(2,1),(3,1),(4,1),(5,1),    (8,1),                    (12,1),    (15,1),(16,1),(17,1),(18,1),(19,1),    (22,1),(23,1),(24,1),(25,1),(26,1),
                       (1,2),                  (5,2),    (8,2),                    (12,2),    (15,2),                                (22,2),                     (26,2),
                       (1,3),                  (5,3),    (8,3),(9,3),       (11,3),(12,3),    (15,3),(16,3),(17,3),(18,3),           (22,3),(23,3),(24,3),(25,3),(26,3),
                       (1,4),                  (5,4),          (9,4),(10,4),(11,4),           (15,4),                                (22,4),       (24,4),
                       (1,5),(2,5),(3,5),(4,5),(5,5),                (10,5),                  (15,5),(16,5),(17,5),(18,5),(19,5),    (22,5),              (25,5)]

        game_over_rects = [[x * 10, y * 10, self.pixel_size, self.pixel_size] for (x, y) in game_coords] + [[x * 10 + 300, y * 10, self.pixel_size, self.pixel_size] for (x, y) in over_coords]
        return game_over_rects
        

class Game:
    def __init__(self, board_size, pixel_size, delay):
        self.disp = Display(board_size, board_size, pixel_size)
        self.snake = Snake(self.disp.get_center(), pixel_size)
        self.clock = pygame.time.Clock()
        self.delay = delay
        self.game_over = False
        self.point_count = 0
        self.papu = (300.0,300.0)
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
    def start(self):
        while not self.game_over:
            pygame.time.delay(self.delay)
            self.clock.tick()
            self.handle_events()
            if not self.pause:
                self.snake.move()
            self.game_over = self.check_collision()
            if self.game_over:
                self.disp.game_over = True
            else:
                self.disp.update(self.snake, list(self.papu), self.pause, self.point_count)
        print('GAME OVER')   
        print('POINTS: ', self.point_count)
    def check_collision(self):
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
        if self.papu == self.snake.pos[0]:
            self.new_papu(self.snake)
            return True
        return False
    def new_papu(self, snake):
        num_of_pixels_width = self.board_size / pixel_size
        num_of_pixels_height = self.board_size / pixel_size
        new_papu_coords = (self.left_boundry + random.randint(0, num_of_pixels_width - 1) * pixel_size, self.upper_boundry + random.randint(0, num_of_pixels_height - 1) * pixel_size)
        if snake is not None and new_papu_coords in snake.pos:
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
