#!/usr/bin/env python3
"""
Snake Game - Android Entry Point
Uses pygame for cross-platform compatibility
"""

import pygame
import sys
import random
import json
import os

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

COLORS = {
    'background': (15, 15, 15),
    'snake': (0, 255, 0),
    'snake_head': (0, 200, 0),
    'food': (255, 0, 0),
    'border': (255, 255, 0),
    'text': (255, 255, 255),
    'score': (0, 255, 255),
    'panel': (50, 50, 50),
}


class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.color = COLORS['snake']
        self.score = 0
        self.grow_count = 0
        self.shape_level = 1

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)

        if new in self.positions:
            return False

        self.positions.insert(0, new)
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.positions.pop()
        return True

    def render(self, surface):
        for i, pos in enumerate(self.positions):
            if i == 0:
                color = COLORS['snake_head']
            else:
                color = COLORS['snake']
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)

            # Draw eyes on head
            if i == 0:
                eye_color = (255, 255, 255)
                eye_size = 4
                offset_x = GRID_SIZE // 2 - eye_size * 2
                offset_y = GRID_SIZE // 2 - eye_size

                if self.direction == (1, 0):  # right
                    left_eye = pygame.Rect(pos[0] * GRID_SIZE + offset_x, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)
                    right_eye = pygame.Rect(pos[0] * GRID_SIZE + GRID_SIZE - offset_x - eye_size * 2, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)
                elif self.direction == (-1, 0):  # left
                    left_eye = pygame.Rect(pos[0] * GRID_SIZE + GRID_SIZE - offset_x - eye_size * 2, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)
                    right_eye = pygame.Rect(pos[0] * GRID_SIZE + offset_x, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)
                elif self.direction == (0, 1):  # down
                    left_eye = pygame.Rect(pos[0] * GRID_SIZE + offset_x, pos[1] * GRID_SIZE + GRID_SIZE - offset_y - eye_size * 2, eye_size * 2, eye_size)
                    right_eye = pygame.Rect(pos[0] * GRID_SIZE + GRID_SIZE - offset_x - eye_size * 2, pos[1] * GRID_SIZE + GRID_SIZE - offset_y - eye_size * 2, eye_size * 2, eye_size)
                else:  # up
                    left_eye = pygame.Rect(pos[0] * GRID_SIZE + offset_x, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)
                    right_eye = pygame.Rect(pos[0] * GRID_SIZE + GRID_SIZE - offset_x - eye_size * 2, pos[1] * GRID_SIZE + offset_y, eye_size * 2, eye_size)

                pygame.draw.ellipse(surface, eye_color, left_eye)
                pygame.draw.ellipse(surface, eye_color, right_eye)


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = COLORS['food']
        self.shape_count = 1
        self.set_shape(1)

    def set_shape(self, count):
        self.shape_count = count

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def render(self, surface):
        for i in range(self.shape_count):
            rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            if self.shape_count > 1:
                for j in range(i):
                    offset = (j + 1) * 3
                    rect2 = pygame.Rect(self.position[0] * GRID_SIZE + offset, self.position[1] * GRID_SIZE + offset, GRID_SIZE - offset * 2, GRID_SIZE - offset * 2)
                    if rect2.width > 0 and rect2.height > 0:
                        pygame.draw.rect(surface, (200, 100, 100), rect2)

    def get_positions(self):
        """Return all positions occupied by this food"""
        positions = []
        for i in range(self.shape_count):
            x, y = self.position
            positions.append((x + i % GRID_WIDTH, y + i // GRID_WIDTH))
        return positions


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.high_score = self.load_high_score()
        self.reset()

    def load_high_score(self):
        try:
            if os.path.exists('snake_data.json'):
                with open('snake_data.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0

    def save_high_score(self):
        try:
            data = {'high_score': self.high_score}
            with open('snake_data.json', 'w') as f:
                json.dump(data, f)
        except:
            pass

    def reset(self):
        self.snake = Snake()
        self.food = Food()
        self.food.randomize_position()
        self.score = 0
        self.game_over = False
        self.message = ""

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake.direction != (0, 1):
            self.snake.direction = (0, -1)
        if keys[pygame.K_DOWN] and self.snake.direction != (0, -1):
            self.snake.direction = (0, 1)
        if keys[pygame.K_LEFT] and self.snake.direction != (1, 0):
            self.snake.direction = (-1, 0)
        if keys[pygame.K_RIGHT] and self.snake.direction != (-1, 0):
            self.snake.direction = (1, 0)

    def update(self):
        if self.game_over:
            return

        self.handle_keys()

        if not self.snake.update():
            self.game_over = True
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            return

        head_pos = self.snake.get_head_position()

        # Check collision with food
        if head_pos == self.food.position:
            self.snake.score += 10
            self.snake.grow_count += 1

            # Increase shape every 3 points
            if self.snake.score % 3 == 0:
                self.food.set_shape(min(4, self.snake.grow_count // 3))
                self.message = "GROWING!"

            self.food.randomize_position()
            while self.food.position in self.snake.positions:
                self.food.randomize_position()

        # Check border collision (wrap enabled, so no border check)
        # But check for game over conditions
        if self.snake.grow_count == 0:
            self.message = ""

    def render(self):
        self.screen.fill(COLORS['background'])

        # Draw border
        pygame.draw.rect(self.screen, COLORS['border'], (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 2)

        # Draw grass/wall pattern
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (SCREEN_WIDTH, y), 1)

        # Draw snake and food
        self.snake.render(self.screen)
        self.food.render(self.screen)

        # Draw score panel
        panel = pygame.Surface((SCREEN_WIDTH, 50))
        panel.fill(COLORS['panel'])
        self.screen.blit(panel, (0, SCREEN_HEIGHT - 50))

        score_text = self.font.render(f"Score: {self.score}", True, COLORS['score'])
        high_text = self.small_font.render(f"High Score: {self.high_score}", True, COLORS['text'])

        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 45))
        self.screen.blit(high_text, (SCREEN_WIDTH - 180, SCREEN_HEIGHT - 40))

        if self.message:
            msg = self.font.render(self.message, True, (255, 255, 0))
            self.screen.blit(msg, (SCREEN_WIDTH // 2 - 80, 10))

        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            game_over_text = self.font.render("GAME OVER!", True, (255, 50, 50))
            score_text = self.font.render(f"Final Score: {self.score}", True, COLORS['text'])
            restart_text = self.small_font.render("Press R to restart or Q to quit", True, COLORS['text'])

            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 40))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if self.game_over and event.key == pygame.K_r:
                        self.reset()
                    if self.game_over and event.key == pygame.K_q:
                        running = False

            self.update()
            self.render()
            self.clock.tick(15)

        self.save_high_score()
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()