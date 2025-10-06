import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
            return False

        # Check self collision
        if new_head in self.body:
            return False

        self.body.insert(0, new_head)

        return True

    def grow(self):
        # Don't remove tail when growing
        pass

    def check_food_collision(self, food_pos):
        return self.body[0] == food_pos

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN,
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                            GRID_SIZE - 1, GRID_SIZE - 1))

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1),
                   random.randint(0, GRID_HEIGHT - 1))
            return pos

    def draw(self, screen):
        pygame.draw.rect(screen, RED,
                        (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE,
                         GRID_SIZE - 1, GRID_SIZE - 1))

# Game class
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.running = True

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.snake.direction != (0, 1):
            self.snake.direction = (0, -1)
        elif keys[pygame.K_DOWN] and self.snake.direction != (0, -1):
            self.snake.direction = (0, 1)
        elif keys[pygame.K_LEFT] and self.snake.direction != (1, 0):
            self.snake.direction = (-1, 0)
        elif keys[pygame.K_RIGHT] and self.snake.direction != (-1, 0):
            self.snake.direction = (1, 0)

    def update(self):
        if not self.snake.move():
            self.running = False

        if self.snake.check_food_collision(self.food.position):
            self.snake.grow()
            self.food.position = self.food.generate_position()
            self.score += 10

        # Remove tail if not growing
        if len(self.snake.body) > 1:
            self.snake.body.pop()

    def draw(self):
        self.screen.fill(BLACK)

        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS

        pygame.quit()
        sys.exit()

# Run the game
if __name__ == '__main__':
    game = Game()
    game.run()