import pygame
import random
import sys

pygame.init()

# Constants
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
COLS = WINDOW_WIDTH // CELL_SIZE   # 32
ROWS = WINDOW_HEIGHT // CELL_SIZE  # 24

# Retro color palette
BLACK      = (0,   0,   0)
GREEN      = (0,   230, 0)
DARK_GREEN = (0,   140, 0)
RED        = (220, 50,  50)
WHITE      = (255, 255, 255)
GRAY       = (30,  30,  30)
YELLOW     = (255, 220, 0)
DIM_YELLOW = (180, 160, 0)

# Moderate speed (cells per second)
FPS = 10

# Directions as (dx, dy)
UP    = (0, -1)
DOWN  = (0,  1)
LEFT  = (-1, 0)
RIGHT = (1,  0)


class Snake:
    def __init__(self):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self._grow = False

    def change_direction(self, new_dir):
        # Prevent 180-degree reversal
        if new_dir[0] != -self.direction[0] or new_dir[1] != -self.direction[1]:
            self.next_direction = new_dir

    def move(self):
        self.direction = self.next_direction
        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        self.body.insert(0, new_head)
        if self._grow:
            self._grow = False
        else:
            self.body.pop()

    def grow(self):
        self._grow = True

    def collides(self):
        hx, hy = self.body[0]
        if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
            return True
        if self.body[0] in self.body[1:]:
            return True
        return False

    def draw(self, surface):
        for i, (x, y) in enumerate(self.body):
            px, py = x * CELL_SIZE, y * CELL_SIZE
            inner = pygame.Rect(px + 1, py + 1, CELL_SIZE - 2, CELL_SIZE - 2)
            if i == 0:
                pygame.draw.rect(surface, GREEN, inner)
                self._draw_eyes(surface, px, py)
            else:
                shade = max(80, 140 - i * 2)
                pygame.draw.rect(surface, (0, shade, 0), inner)

    def _draw_eyes(self, surface, px, py):
        s = 3
        d = self.direction
        if d == RIGHT:
            eyes = [(px + CELL_SIZE - 7, py + 4), (px + CELL_SIZE - 7, py + CELL_SIZE - 7)]
        elif d == LEFT:
            eyes = [(px + 4, py + 4), (px + 4, py + CELL_SIZE - 7)]
        elif d == UP:
            eyes = [(px + 4, py + 4), (px + CELL_SIZE - 7, py + 4)]
        else:
            eyes = [(px + 4, py + CELL_SIZE - 7), (px + CELL_SIZE - 7, py + CELL_SIZE - 7)]
        for ex, ey in eyes:
            pygame.draw.rect(surface, BLACK, (ex, ey, s, s))


class Food:
    def __init__(self, snake_body):
        self.pos = self._random(snake_body)

    def _random(self, snake_body):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in snake_body:
                return pos

    def respawn(self, snake_body):
        self.pos = self._random(snake_body)

    def draw(self, surface):
        px, py = self.pos[0] * CELL_SIZE, self.pos[1] * CELL_SIZE
        pygame.draw.rect(surface, RED, (px + 3, py + 5, CELL_SIZE - 6, CELL_SIZE - 7))
        pygame.draw.rect(surface, DARK_GREEN, (px + CELL_SIZE // 2 - 1, py + 2, 2, 4))
        pygame.draw.rect(surface, (255, 120, 120), (px + 5, py + 7, 3, 3))


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("SNAKE  —  Retro Edition")
        self.clock = pygame.time.Clock()
        self.font_xl   = pygame.font.Font(None, 80)
        self.font_lg   = pygame.font.Font(None, 48)
        self.font_md   = pygame.font.Font(None, 32)
        self.font_sm   = pygame.font.Font(None, 22)
        self.high_score = 0
        self._reset()

    def _reset(self):
        self.snake     = Snake()
        self.food      = Food(self.snake.body)
        self.score     = 0
        self.game_over = False
        self.paused    = False

    def _draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))

    def _draw_hud(self):
        score_surf = self.font_md.render(f"SCORE  {self.score}", True, WHITE)
        hi_surf    = self.font_sm.render(f"BEST  {self.high_score}", True, DIM_YELLOW)
        self.screen.blit(score_surf, (8, 6))
        self.screen.blit(hi_surf,    (8, 34))

    def _text_centered(self, surf, y):
        self.screen.blit(surf, (WINDOW_WIDTH // 2 - surf.get_width() // 2, y))

    def _draw_overlay(self, alpha=160):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        self.screen.blit(overlay, (0, 0))

    def _draw_start_screen(self):
        self.screen.fill(BLACK)
        self._draw_grid()
        self._text_centered(self.font_xl.render("SNAKE",         True, GREEN),      120)
        self._text_centered(self.font_md.render("RETRO EDITION", True, DARK_GREEN), 200)
        self._text_centered(self.font_md.render("Press SPACE to start", True, YELLOW), 300)
        self._text_centered(self.font_sm.render("Arrow keys / WASD  •  P = Pause  •  Q = Quit", True, WHITE), 350)

    def _draw_game_over(self):
        self._draw_overlay()
        self._text_centered(self.font_xl.render("GAME OVER", True, RED), 160)
        self._text_centered(self.font_lg.render(f"Score:  {self.score}", True, WHITE), 260)
        if self.score == self.high_score and self.score > 0:
            self._text_centered(self.font_md.render("NEW HIGH SCORE!", True, YELLOW), 310)
        self._text_centered(self.font_md.render("R = Restart    Q = Quit", True, DIM_YELLOW), 370)

    def _draw_pause(self):
        self._draw_overlay(120)
        self._text_centered(self.font_lg.render("PAUSED", True, YELLOW), WINDOW_HEIGHT // 2 - 24)
        self._text_centered(self.font_sm.render("P to resume", True, WHITE), WINDOW_HEIGHT // 2 + 30)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self._game_loop()
                        return
                    if event.key == pygame.K_q:
                        pygame.quit(); sys.exit()
            self._draw_start_screen()
            pygame.display.flip()
            self.clock.tick(30)

    def _game_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self._reset()
                        elif event.key == pygame.K_q:
                            pygame.quit(); sys.exit()
                    else:
                        if   event.key in (pygame.K_UP,    pygame.K_w): self.snake.change_direction(UP)
                        elif event.key in (pygame.K_DOWN,  pygame.K_s): self.snake.change_direction(DOWN)
                        elif event.key in (pygame.K_LEFT,  pygame.K_a): self.snake.change_direction(LEFT)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d): self.snake.change_direction(RIGHT)
                        elif event.key == pygame.K_p: self.paused = not self.paused
                        elif event.key == pygame.K_q: pygame.quit(); sys.exit()

            if not self.game_over and not self.paused:
                self.snake.move()
                if self.snake.collides():
                    self.game_over = True
                    if self.score > self.high_score:
                        self.high_score = self.score
                elif self.snake.body[0] == self.food.pos:
                    self.snake.grow()
                    self.score += 10
                    self.food.respawn(self.snake.body)

            self.screen.fill(BLACK)
            self._draw_grid()
            self.food.draw(self.screen)
            self.snake.draw(self.screen)
            self._draw_hud()

            if self.game_over:
                self._draw_game_over()
            elif self.paused:
                self._draw_pause()

            pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
