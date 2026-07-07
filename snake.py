#!/usr/bin/env python3
"""
Snake Game - Terminal-based version using curses
"""

import curses
import random
import time
import json
import os

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.stdscr.timeout(100)

        self.shapes = ['single', 'double', 'triple', 'quadruple']
        self.difficulties = {'easy': 150, 'medium': 100, 'hard': 50}

        self.reset_game()

    def reset_game(self):
        self.snake = [(10, 5), (10, 4), (10, 3)]
        self.direction = curses.KEY_RIGHT
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False
        self.high_score = self.load_high_score()
        self.speed = self.difficulties.get('medium', 100)
        self.growing = False
        self.grow_count = 0
        self.shape_index = 0
        self.max_shapes_seen = 0
        self.shapes_seen = []

    def load_high_score(self):
        try:
            with open('snake_data.json', 'r') as f:
                data = json.load(f)
                return data.get('high_score', 0)
        except:
            return 0

    def save_high_score(self):
        try:
            data = {'high_score': self.high_score}
            with open('snake_data.json', 'w') as f:
                json.dump(data, f)
        except:
            pass

    def generate_food(self):
        while True:
            food = (random.randint(1, 27), random.randint(1, 56))
            if food not in self.snake:
                return food

    def place_food(self, shape=None):
        if shape:
            foods = [self.generate_food() for _ in range(shape)]
            return foods
        return [self.generate_food()]

    def draw_borders(self):
        self.stdscr.border()

    def draw_snake(self):
        for i, (y, x) in enumerate(self.snake):
            if i == 0:
                self.stdscr.addch(y, x, '@')
            else:
                self.stdscr.addch(y, x, 'o')

    def draw_food(self, foods):
        for y, x in foods:
            self.stdscr.addch(y, x, 'X')

    def update_speed(self):
        if len(self.snake) >= self.max_shapes_seen:
            if self.shape_index < len(self.shapes) - 1:
                self.shape_index += 1
                self.max_shapes_seen += 1
                self.growing = True
                self.grow_count = len(self.shapes[self.shape_index])
                self.speed = self.difficulties.get('hard', 50)

    def draw_info(self):
        info_y = 30 // 2
        self.stdscr.addstr(info_y, 20, f"Score: {self.score}")
        self.stdscr.addstr(info_y + 1, 20, f"High: {self.high_score}")
        self.stdscr.addstr(info_y + 2, 20, f"Shape: {self.shapes[self.shape_index].upper()}")

    def game_loop(self):
        while not self.game_over:
            self.stdscr.clear()

            self.draw_borders()
            self.draw_info()
            self.draw_snake()

            if self.growing and self.grow_count > 0:
                foods = self.place_food()
            else:
                foods = self.food

            self.draw_food(foods)

            key = self.stdscr.getch()
            if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self.direction = key

            head_y, head_x = self.snake[0]

            if self.direction == curses.KEY_UP:
                head_y -= 1
            elif self.direction == curses.KEY_DOWN:
                head_y += 1
            elif self.direction == curses.KEY_LEFT:
                head_x -= 1
            elif self.direction == curses.KEY_RIGHT:
                head_x += 1

            new_head = (head_y, head_x)

            if (head_y == 0 or head_y == 28 or head_x == 0 or head_x == 57 or
                new_head in self.snake):
                self.game_over = True
                break

            self.snake.insert(0, new_head)

            current_foods = foods if self.growing and self.grow_count > 0 else self.food

            if new_head in current_foods:
                self.score += 10
                if self.growing:
                    self.grow_count -= 1
                    if self.grow_count == 0:
                        self.growing = False
                        self.update_speed()
                        current_foods = self.food = self.generate_food()
                else:
                    self.food = self.generate_food()
            else:
                if not (self.growing and self.grow_count > 0):
                    self.snake.pop()

            self.stdscr.refresh()
            time.sleep(self.speed / 1000.0)

        self.save_high_score()
        self.show_game_over()

    def show_game_over(self):
        self.stdscr.clear()
        self.stdscr.addstr(14, 25, "GAME OVER!")
        self.stdscr.addstr(16, 20, f"Final Score: {self.score}")
        if self.score > self.high_score:
            self.stdscr.addstr(17, 20, "NEW HIGH SCORE!")
            self.high_score = self.score
            self.save_high_score()
        self.stdscr.addstr(18, 15, "Press any key to play again, Q to quit")
        self.stdscr.refresh()

        key = self.stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            return
        else:
            self.reset_game()
            self.game_loop()


def main():
    stdscr = curses.initscr()
    try:
        game = SnakeGame(stdscr)
        game.game_loop()
    finally:
        curses.endwin()


if __name__ == '__main__':
    main()