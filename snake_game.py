# Total dimensions: 39 square width, 30 square height
# Box dimensions: 37 square width, 27 square height
# Left, right, and top border are 1 square thick; bottom border is 2 squares thick

import pygame, mechanics

BORDER_WIDTH = 39

BORDER_COLOR = pygame.Color(8, 62, 112)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
GRAY = pygame.Color(80, 80, 80)
LIGHT_GRAY = pygame.Color(128, 128, 128)

class SnakeGame:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        self._screen = None
        self._running = True
        self._high_score = 1

        infoObject = pygame.display.Info()
        self._width = infoObject.current_w * (26 / 57)
        self._height = infoObject.current_h * (75 / 139)
        self._square_side = self._width // BORDER_WIDTH

        self._state = mechanics.State()

    def run(self) -> None:
        '''Run game instance'''

        try:
            clock = pygame.time.Clock()
            self._resize((self._width, self._height))

            while self._running:
                clock.tick(12)

                self._setup()
                self._handle_events()
                if not self._running:
                    break
                if not self._state.update():
                    self._end_game()
                    if not self._running:
                        break
                self._draw_elements()
                
                pygame.display.flip()
        finally:
            pygame.quit()

    def _setup(self) -> None:
        '''Draw basic game elements on screen'''

        self._screen.fill(BLACK)

        self._draw_borders()
        self._display_length()
        self._display_high_score()

    def _handle_events(self) -> None:
        '''Handles user input'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                break
            elif event.type == pygame.VIDEORESIZE:
                self._resize(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._state.up()
                elif event.key == pygame.K_LEFT:
                    self._state.left()
                elif event.key == pygame.K_RIGHT:
                    self._state.right()
                elif event.key == pygame.K_DOWN:
                    self._state.down()

    def _draw_elements(self) -> None:
        '''Draws snake, apple, and background'''

        board = self._state.get_board()
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == "B":
                    self._draw_square([j, i], BLACK)
                elif board[i][j] == "G":
                    self._draw_square([j, i], GREEN)
                elif board[i][j] == "R":
                    self._draw_square([j, i], RED)

    # ****************
    # HELPER FUNCTIONS
    # ****************

    def _resize(self, size: tuple[int, int]) -> None:
        '''Resizes the screen'''

        self._screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self._width = self._screen.get_width()
        self._height = self._screen.get_height()
        self._square_side = self._width // BORDER_WIDTH

    def _draw_borders(self) -> None:
        '''Draws the blue borders on the screen'''

        top = pygame.Rect(0, 0, self._width, self._square_side)
        pygame.draw.rect(self._screen, BORDER_COLOR, top)
        left = pygame.Rect(0, self._square_side, self._square_side, self._height)
        pygame.draw.rect(self._screen, BORDER_COLOR, left)
        right = pygame.Rect(self._width - self._square_side, self._square_side, self._square_side, self._height)
        pygame.draw.rect(self._screen, BORDER_COLOR, right)
        bottom = pygame.Rect(self._square_side, self._height - (self._square_side * 2), self._width - self._square_side, self._square_side * 2)
        pygame.draw.rect(self._screen, BORDER_COLOR, bottom)

    def _display_length(self) -> None:
        '''Displays the snake's current length on the bottom-left of the screen'''

        font = pygame.font.SysFont("arial", int(1.1 * self._square_side))
        current_length_text = font.render("Length: " + str(self._state.get_display_length()), True, WHITE)
        current_length_textRect = current_length_text.get_rect()
        current_length_textRect.bottomleft = (self._square_side, 2 * self._height // 2 - .5 * self._square_side)
        self._screen.blit(current_length_text, current_length_textRect)

    def _display_high_score(self) -> None:
        '''Displays the user's current high score on the bottom-right of the screen'''

        font = pygame.font.SysFont("arial", int(1.1 * self._square_side))
        high_score_text = font.render("Best: " + str(self._high_score), True, WHITE)
        high_score_textRect = high_score_text.get_rect()
        high_score_textRect.bottomright = (self._width - 1 * self._square_side, 2 * self._height // 2 - .5 * self._square_side)
        self._screen.blit(high_score_text, high_score_textRect)

    def _draw_square(self, part: list[int], color: pygame.Color) -> None:
        '''Draws a sqare of the given color at the given coordinates'''

        rect = pygame.Rect((part[0]+1) * self._square_side, (part[1]+1) * self._square_side, .95 * self._square_side, .95 * self._square_side)
        pygame.draw.rect(self._screen, color, rect)

    def _end_game(self) -> None:
        '''Updates the high score if necessary and displays the end screen'''

        display_length = self._state.get_display_length()
        if display_length > self._high_score:
            self._high_score = display_length

        rerun = False
        try:
            while self._running:
                self._setup()
                self._draw_elements()

                play_again_button = self._display_end_screen_text()
                rerun = self._end_game_handle_events(play_again_button)

                if not self._running:
                    break

                pygame.display.flip()
        finally:
            if rerun:
                self._running = True
                self._state.reset()
                self.run()
            else:
                pygame.quit()

    def _display_end_screen_text(self) -> pygame.rect.Rect:
        '''Displays text for the end game'''

        font = pygame.font.SysFont("arial", int(1.1 * self._square_side))
        
        self._display_game_over_text(font)
        self._display_end_length_text(font)

        font = pygame.font.SysFont("arial", int(1.5 * self._square_side))

        play_again_button = self._display_play_again_button(font)

        return play_again_button
    
    def _display_game_over_text(self, font: pygame.font) -> None:
        '''Displays the game over text'''

        game_over_text = font.render("GAME OVER", True, WHITE, BLACK)
        game_over_textRect = game_over_text.get_rect()
        game_over_textRect.center = (self._width // 2, self._height // 2 - 4 * self._square_side)

        self._screen.blit(game_over_text, game_over_textRect)

    def _display_end_length_text(self, font: pygame.font) -> None:
        '''Displays the snake's final length text'''

        length_text = font.render("Length: " + str(self._state.get_display_length()), True, WHITE, BLACK)
        length_textRect = length_text.get_rect()
        length_textRect.center = (self._width // 2, self._height // 2 - 2 * self._square_side)

        self._screen.blit(length_text, length_textRect)

    def _display_play_again_button(self, font: pygame.font) -> pygame.rect.Rect:
        '''Displays the play again button and changes the button's shade based on user input'''

        play_again_text = font.render(" Play Again ", True, WHITE, GRAY)
        play_again_button = play_again_text.get_rect()
        play_again_button.center = (self._width // 2, self._height // 2 + 2 * self._square_side)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if play_again_button.x <= mouse_x <= play_again_button.x + play_again_button.width and play_again_button.y <= mouse_y <= play_again_button.y + play_again_button.height:
            play_again_text = font.render(" Play Again ", True, WHITE, LIGHT_GRAY)
        else:
            play_again_text = font.render(" Play Again ", True, WHITE, GRAY)

        self._screen.blit(play_again_text, play_again_button)

        return play_again_button
    
    def _end_game_handle_events(self, play_again_button: pygame.rect.Rect) -> bool:
        '''Handles user input for the end of the game and returns whether to start a new game'''

        rerun = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._resize(event.size)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    self._running = False
                    rerun = True
        return rerun

if __name__ == "__main__":
    SnakeGame().run()