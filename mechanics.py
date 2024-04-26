from random import random, randint

ROWS = 27
COLS = 37
MIDDLE = (14, 19) # row, column

class State:

    def __init__(self):
        self._board = self._create_board()
        self._high_score = 1

        self._snake_color = "G"
        self._snake_coords = [MIDDLE]
        self._board[MIDDLE[0]][MIDDLE[1]] = self._snake_color
        self._direction = None
        self._snake_length = 1
        self._display_length = 1
        self._grow_coords = None

        self._new_powerup = False
        self._powerup_timer = 0

        self._apple_coords = ()
        self._apple_color = None
    
    def update(self) -> bool:
        '''Updates game variables'''
        
        self._eat()
        if not self._move():
            return False
        self._grow_snake()
        self._set_snake_color()
        self._spawn_apple()

        return True
    
    def up(self) -> None:
        '''Handles up arrow input'''

        if self._snake_length == 1 or self._direction != "down":
            self._direction = "up"

    def left(self) -> None:
        '''Handles left arrow input'''

        if self._snake_length == 1 or self._direction != "right":
            self._direction = "left"

    def right(self) -> None:
        '''Handles right arrow input'''
        
        if self._snake_length == 1 or self._direction != "left":
            self._direction = "right"

    def down(self) -> None:
        '''Handles down arrow input'''

        if self._snake_length == 1 or self._direction != "up":
            self._direction = "down"

    def get_board(self) -> list[list[str]]:
        '''Returns the board'''
        
        return self._board

    def get_display_length(self) -> int:
        '''Returns display length''' 

        return self._display_length
    
    def reset(self) -> None:
        '''Resets necessary game variables'''

        self._board = self._create_board()

        self._snake_color = "G"
        self._snake_coords = [MIDDLE]
        self._board[MIDDLE[0]][MIDDLE[1]] = self._snake_color
        self._direction = None
        self._snake_length = 1
        self._display_length = 1
        self._grow_coords = None

        self._new_powerup = False
        self._powerup_timer = 0

        self._apple_coords = ()

    def print_board(self) -> None:
        '''Prints the board to the terminal'''

        for row in self._board:
            for val in row:
                print(val + " ", end="")
            print()

    def _create_board(self) -> list[list[str]]:
        '''Initializes an empty board'''

        return [["B" for i in range(COLS)] for j in range(ROWS)]

    def _eat(self) -> None:
        '''Eats the apple if the snake's head overlaps with the apple'''

        if (self._snake_coords[0] == self._apple_coords):
            self._apple_coords = ()
            self._display_length += 8 if self._apple_color == "Y" else 4
            self._grow_coords = self._snake_coords[-1]

            if self._apple_color != "R":
                self._new_powerup = True

    def _move(self) -> bool:
        '''Moves the snake by one square if possible'''

        if self._direction is None:
            return True

        new_pos = self._get_next_pos()
        if self._check_game_over(new_pos):
            return False
        else:
            new_head_row, new_head_col = new_pos
            old_tail_row, old_tail_col = self._snake_coords[-1]
            self._board[new_head_row][new_head_col] = self._snake_color
            self._board[old_tail_row][old_tail_col] = "B"

            for i in range(len(self._snake_coords)):
                temp = self._snake_coords[i]
                self._snake_coords[i] = new_pos
                new_pos = temp

            return True

    def _grow_snake(self) -> None:
        '''Increases the length of the snake by one if needed'''
        
        if self._snake_length != self._display_length:
            self._snake_coords.append(self._grow_coords)
            row, col = self._grow_coords
            self._board[row][col] = self._snake_color
            self._snake_length += 1

    def _set_snake_color(self) -> None:
        '''Determines and sets the snake's color'''

        if self._new_powerup:
            self._snake_color = "C"
            self._powerup_timer = 6
            self._update_color()
            self._new_powerup = False
        elif self._powerup_timer == 1:
            self._snake_color = "G"
            self._update_color()
            self._powerup_timer -= 1
        elif self._powerup_timer > 1:
            self._powerup_timer -= 1

    def _spawn_apple(self) -> None:
        '''Spawns the apple at a random location'''

        if self._apple_coords:
            return
        
        row, col = self._generate_apple_coords()
        self._apple_coords = (row, col)
        self._apple_color = "R" if random() <= 0.80 else "Y" 
        self._board[row][col] = self._apple_color

    # ****************
    # HELPER FUNCTIONS
    # ****************
    
    def _get_next_pos(self) -> tuple[int, int]:
        '''Retrieves the next position of the snake's head based on its current direction'''

        next_pos = None

        head_row, head_col = self._snake_coords[0]
        if self._direction is None:
            next_pos = self._snake_coords[0]
        elif self._direction == "up":
            next_pos = (head_row - 1, head_col)
        elif self._direction == "left":
            next_pos = (head_row, head_col - 1)
        elif self._direction == "right":
            next_pos = (head_row, head_col + 1)
        else:
            next_pos = (head_row + 1, head_col)

        return next_pos
    
    def _check_game_over(self, next_pos: tuple[int, int]) -> bool:
        '''Determines if the game is over'''

        row = next_pos[0]
        col = next_pos[1]

        if (row == -1 or row == 27):
            return True
        if (col == -1 or col == 37):
            return True
        
        return self._board[row][col] == self._snake_color
    
    def _generate_apple_coords(self) -> tuple[int]:
        '''Generates random coordinates for the apple that do not overlap with the snake'''
        
        row = randint(0, ROWS-1)
        col = randint(0, COLS-1)

        if self._board[row][col] == self._snake_color:
            while True:
                row = randint(0, ROWS-1)
                col = randint(0, COLS-1)
                if self._board[row][col] != self._snake_color:
                    break
                
        return row, col
    
    def _update_color(self) -> None:
        '''Updates the snake's color on the board'''

        for coord in self._snake_coords:
            row, col = coord
            self._board[row][col] = self._snake_color