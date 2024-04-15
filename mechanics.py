from random import randint

ROWS = 27
COLS = 37
MIDDLE = (19, 14)

class State:

    def __init__(self):
        self._board = self._create_board()
        self._high_score = 1

        self._snake_coords = [MIDDLE]
        self._board[MIDDLE[1]][MIDDLE[0]] = "G"
        self._direction = None
        self._snake_length = 1
        self._display_length = 1
        self._grow_coords = None

        self._apple_coords = ()
    
    def update(self) -> bool:
        '''Updates game variables'''

        if not self._move():
            return False
        self._eat()
        self._grow_snake()
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

        self._snake_coords = [MIDDLE]
        self._board[MIDDLE[1]][MIDDLE[0]] = "G"
        self._direction = None
        self._snake_length = 1
        self._display_length = 1
        self._grow_coords = None

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

    def _move(self) -> bool:
        '''Moves the snake by one square if possible'''

        if self._direction is None:
            return True

        next_pos = self._get_next_pos()
        if self._check_game_over(next_pos):
            return False
        else:
            head_col, head_row = next_pos
            old_tail_col, old_tail_row = self._snake_coords[-1]
            self._board[head_row][head_col] = "G"
            self._board[old_tail_row][old_tail_col] = "B"

            self._snake_coords[0] = next_pos
            for i in reversed(range(1, len(self._snake_coords))):
                self._snake_coords[i] = self._snake_coords[i-1]
            return True

    def _eat(self) -> None:
        '''Eats the apple if the snake's head overlaps with the apple'''

        if (self._snake_coords[0] == self._apple_coords):
            self._apple_coords = ()
            self._display_length += 4
            self._grow_coords = self._snake_coords[-1]

    def _grow_snake(self) -> None:
        '''Increases the length of the snake by one if needed'''

        if self._snake_length != self._display_length:
            self._snake_coords.append(self._grow_coords)
            col, row = self._grow_coords
            self._board[row][col] = "G"
            self._snake_length += 1

    def _spawn_apple(self) -> None:
        '''Spawns the apple at a random location'''

        if self._apple_coords:
            return
        
        x, y = self._generate_apple_coords()
        self._apple_coords = (x, y)
        self._board[y][x] = "R"

    # ****************
    # HELPER FUNCTIONS
    # ****************
    
    def _get_next_pos(self) -> tuple[int, int]:
        '''Retrieves the next position of the snake's head based on its current direction'''

        next_pos = None

        if self._direction is None:
            next_pos = self._snake_coords[0]
        elif self._direction == "up":
            next_pos = (self._snake_coords[0][0], self._snake_coords[0][1] - 1)
        elif self._direction == "left":
            next_pos = (self._snake_coords[0][0] - 1, self._snake_coords[0][1])
        elif self._direction == "right":
            next_pos = (self._snake_coords[0][0] + 1, self._snake_coords[0][1])
        else:
            next_pos = (self._snake_coords[0][0], self._snake_coords[0][1] + 1)

        return next_pos
    
    def _check_game_over(self, next_pos: tuple[int, int]) -> bool:
        '''Determines if the game is over'''

        col = next_pos[0]
        row = next_pos[1]

        if (col == -1 or col == 37):
            return True
        if (row == -1 or row == 27):
            return True
        
        return self._board[row][col] == "G"
    
    def _generate_apple_coords(self) -> tuple[int]:
        '''Generates random coordinates for the apple that do not overlap with the snake'''
        
        x = randint(0, COLS-1)
        y = randint(0, ROWS-1)

        if self._board[y][x] == "G":
            while True:
                x = randint(0, COLS-1)
                y = randint(0, ROWS-1)
                if self._board[y][x] != "G":
                    break
                
        return x, y