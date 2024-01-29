# Total dimensions: 39 square width, 30 square height
# Box dimensions: 37 square width, 27 square height
# Left, right, and top border are 1 square thick; bottom border is 2 squares thick

import pygame
from random import randint

INITIAL_WIDTH = 780
INITIAL_HEIGHT = 600
SQUARE_SCREEN_WIDTH = 39
SQUARE_SCREEN_MIDDLE = (19, 14)
SQUARE_BLACK_BOX_WIDTH = 37
SQUARE_BLACK_BOX_HEIGHT = 27

BORDER_COLOR = pygame.Color(8, 62, 112)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GRAY = pygame.Color(80, 80, 80)
LIGHT_GRAY = pygame.Color(128, 128, 128)

class SnakeGame:
    def __init__(self, high_score = 1, width = 0, height = 0):
        '''Initialize game variables'''

        self.screen = None
        self.running = True

        self.high_score = high_score

        self.width = width
        self.height = height
        self.square_side = self.width // SQUARE_SCREEN_WIDTH

        self.snake_coords = [SQUARE_SCREEN_MIDDLE]
        self.direction = None
        self.snake_length = 1
        self.grow_length = 1
        self.grow_coords = None

        self.apple = False
        self.apple_coords = ()

    def run(self) -> None:
        '''Run game instance'''

        pygame.init()

        try:
            clock = pygame.time.Clock()

            if self.width == 0 and self.height == 0:
                infoObject = pygame.display.Info()
                self.width = infoObject.current_w * (26 / 57)
                self.height = infoObject.current_h * (75 / 139)

            self.resize((self.width, self.height))

            while self.running:
                clock.tick(12)

                self.setup()
                self.grow_snake()
                self.draw_snake()
                self.spawn_apple()
                self.handle_events()
                self.move()
                self.try_eat()

                if not self.running:
                    break

                pygame.display.flip()
        finally:
            pygame.quit()

    def setup(self) -> None:
        '''Draw basic game elements on screen'''

        self.screen.fill(BLACK)

        self.draw_borders()
        self.display_length()
        self.display_high_score()

    def grow_snake(self) -> None:
        '''Increases the length of the snake by one square if necessary'''

        if self.snake_length != self.grow_length:
            self.snake_coords.append(self.grow_coords)
            self.snake_length += 1

    def draw_snake(self) -> None:
        '''Draws the snake on the screen'''

        for part in self.snake_coords:
            self.draw_square(part, GREEN)

    def spawn_apple(self) -> None:
        '''Draws the apple on the screen'''

        if self.apple:
            self.draw_square(self.apple_coords, RED)
            return
        
        x, y = self.generate_apple_coords()
        self.apple_coords = (x, y)
        self.draw_square(self.apple_coords, RED)

        self.apple = True

    def handle_events(self) -> None:
        '''Handles user input'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if self.snake_length == 1 or self.direction != "down":
                        self.direction = "up"
                elif event.key == pygame.K_LEFT:
                    if self.snake_length == 1 or self.direction != "right":
                        self.direction = "left"
                elif event.key == pygame.K_RIGHT:
                    if self.snake_length == 1 or self.direction != "left":
                        self.direction = "right"
                elif event.key == pygame.K_DOWN:
                    if self.snake_length == 1 or self.direction != "up":
                        self.direction = "down"
    
    def move(self) -> None:
        '''Attempts to move the snake by one square'''

        if self.direction is None:
            return
        
        next_pos = self.get_next_pos()
        if self.check_game_over(next_pos):
            self.end_game()
        else:
            self.snake_coords[0] = next_pos
            for i in reversed(range(1, len(self.snake_coords))):
                self.snake_coords[i] = self.snake_coords[i-1]

    def try_eat(self) -> None:
        '''Eats the apple if the snake's head makes contact with the apple'''

        if (self.snake_coords[0] == self.apple_coords):
            self.apple = False
            self.grow_length += 4
            self.grow_coords = self.snake_coords[-1]

    # ****************
    # HELPER FUNCTIONS
    # ****************

    def resize(self, size: tuple[int, int]) -> None:
        '''Resizes the screen'''

        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        self.square_side = self.width // SQUARE_SCREEN_WIDTH

    def draw_borders(self) -> None:
        '''Draws the blue borders on the screen'''

        top = pygame.Rect(0, 0, self.width, self.square_side)
        pygame.draw.rect(self.screen, BORDER_COLOR, top)
        left = pygame.Rect(0, self.square_side, self.square_side, self.height)
        pygame.draw.rect(self.screen, BORDER_COLOR, left)
        right = pygame.Rect(self.width - self.square_side, self.square_side, self.square_side, self.height)
        pygame.draw.rect(self.screen, BORDER_COLOR, right)
        bottom = pygame.Rect(self.square_side, self.height - (self.square_side * 2), self.width - self.square_side, self.square_side * 2)
        pygame.draw.rect(self.screen, BORDER_COLOR, bottom)

    def display_length(self) -> None:
        '''Displays the snake's current length on the bottom-left of the screen'''

        font = pygame.font.SysFont("arial", int(1.1 * self.square_side))
        current_length_text = font.render("Length: " + str(self.grow_length), True, WHITE)
        current_length_textRect = current_length_text.get_rect()
        current_length_textRect.bottomleft = (self.square_side, 2 * self.height // 2 - .5 * self.square_side)
        self.screen.blit(current_length_text, current_length_textRect)

    def display_high_score(self) -> None:
        '''Displays the user's current high score on the bottom-right of the screen'''

        font = pygame.font.SysFont("arial", int(1.1 * self.square_side))
        high_score_text = font.render("Best: " + str(self.high_score), True, WHITE)
        high_score_textRect = high_score_text.get_rect()
        high_score_textRect.bottomright = (self.width - 1 * self.square_side, 2 * self.height // 2 - .5 * self.square_side)
        self.screen.blit(high_score_text, high_score_textRect)

    def draw_square(self, part: list[int], color: pygame.Color) -> None:
        '''Draws a sqare of the given color at the given coordinates'''

        rect = pygame.Rect(part[0] * self.square_side, part[1] * self.square_side, .95 * self.square_side, .95 * self.square_side)
        pygame.draw.rect(self.screen, color, rect)

    def generate_apple_coords(self) -> tuple[int]:
        '''Generates random coordinates for the apple that do not intersect the snake'''

        x = randint(1, SQUARE_BLACK_BOX_WIDTH)
        y = randint(1, SQUARE_BLACK_BOX_HEIGHT)

        if self.screen.get_at((x * self.square_side, y * self.square_side)) == GREEN:
            while True:
                x = randint(1, SQUARE_BLACK_BOX_WIDTH)
                y = randint(1, SQUARE_BLACK_BOX_HEIGHT)
                if self.screen.get_at((x * self.square_side, y * self.square_side)) != GREEN:
                    break
                
        return x, y
    
    def get_next_pos(self) -> tuple[int, int]:
        '''Retrieves the next position of the snake's head based on its current direction'''

        next_pos = None

        if self.direction is None:
            next_pos = self.snake_coords[0]
        elif self.direction == "up":
            next_pos = (self.snake_coords[0][0], self.snake_coords[0][1] - 1)
        elif self.direction == "left":
            next_pos = (self.snake_coords[0][0] - 1, self.snake_coords[0][1])
        elif self.direction == "right":
            next_pos = (self.snake_coords[0][0] + 1, self.snake_coords[0][1])
        else:
            next_pos = (self.snake_coords[0][0], self.snake_coords[0][1] + 1)

        return next_pos
    
    def check_game_over(self, next_pos: tuple[int, int]) -> bool:
        '''Determines if the game is over'''

        x_coord = next_pos[0]
        y_coord = next_pos[1]

        if (x_coord == 0 or x_coord == 38):
            return True
        if (y_coord == 0 or y_coord == 28):
            return True
        
        if (self.screen.get_at((x_coord * self.square_side, 
                                y_coord * self.square_side)) == GREEN):
            return True
        
        return False
    
    def end_game(self) -> None:
        '''Updates the high score if necessary and displays the end screen'''

        if self.grow_length > self.high_score:
            self.high_score = self.grow_length

        rerun = False
        try:
            while self.running:
                self.setup()
                self.draw_snake()
                self.spawn_apple()

                play_again_button = self.display_end_screen_text()
                rerun = self.end_game_handle_events(play_again_button)

                if not self.running:
                    break

                pygame.display.flip()
        finally:
            pygame.quit()
            if rerun:
                SnakeGame(self.high_score, self.width, self.height).run()

    def end_game_handle_events(self, play_again_button: pygame.rect.Rect) -> bool:
        '''Handles user input for the end of the game and returns whether to start a new game or not'''

        rerun = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    self.running = False
                    rerun = True
        return rerun

    def display_end_screen_text(self) -> pygame.rect.Rect:
        '''Displays text for the end game'''

        font = pygame.font.SysFont("arial", int(1.1 * self.square_side))
        
        self.display_game_over_text(font)
        self.display_end_length_text(font)

        font = pygame.font.SysFont("arial", int(1.5 * self.square_side))

        play_again_button = self.display_play_again_button(font)

        return play_again_button

    def display_game_over_text(self, font: pygame.font) -> None:
        '''Displays the game over text'''

        game_over_text = font.render("GAME OVER", True, WHITE, BLACK)
        game_over_textRect = game_over_text.get_rect()
        game_over_textRect.center = (self.width // 2, self.height // 2 - 4 * self.square_side)

        self.screen.blit(game_over_text, game_over_textRect)

    def display_end_length_text(self, font: pygame.font) -> None:
        '''Displays the snake's final length text'''

        length_text = font.render("Length: " + str(self.grow_length), True, WHITE, BLACK)
        length_textRect = length_text.get_rect()
        length_textRect.center = (self.width // 2, self.height // 2 - 2 * self.square_side)

        self.screen.blit(length_text, length_textRect)

    def display_play_again_button(self, font: pygame.font) -> pygame.rect.Rect:
        '''Displays the play again button and changes the button's shade based on user input'''

        play_again_text = font.render(" Play Again ", True, WHITE, GRAY)
        play_again_button = play_again_text.get_rect()
        play_again_button.center = (self.width // 2, self.height // 2 + 2 * self.square_side)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if play_again_button.x <= mouse_x <= play_again_button.x + play_again_button.width and play_again_button.y <= mouse_y <= play_again_button.y + play_again_button.height:
            play_again_text = font.render(" Play Again ", True, WHITE, LIGHT_GRAY)
        else:
            play_again_text = font.render(" Play Again ", True, WHITE, GRAY)

        self.screen.blit(play_again_text, play_again_button)

        return play_again_button

if __name__ == '__main__':
    SnakeGame().run()