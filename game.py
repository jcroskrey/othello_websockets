
class Othello:
    def __init__(self, starting_grid: list[list[int | None]]=None, starting_move: int = 0):
        self.grid = starting_grid
        if not self.grid:
            self.grid = self.get_default_starting_grid()
        self.move = starting_move
        self.white_score = 2
        self.black_score = 2
        self.ROWS = len(self.grid)
        self.COLS = len(self.grid[0])
        self.PLAYER1 = 'black'
        self.PLAYER2 = 'white'
        self.directions = [[0, 1], [1, 0], [0, -1], [-1, 0], [1, 1], [-1, -1], [1, -1], [-1, 1]]

    def get_default_starting_grid(self) -> list[list[int | None]]:
        grid = [[None] * 8 for _ in range(8)]
        grid[3][3] = 0 # 0 is white
        grid[3][4] = 1 # 1 is black
        grid[4][3] = 1
        grid[4][4] = 0
        return grid
    
    def make_move(self, player: int, row: int, col: int) -> dict: 
        curr_player_color = self.PLAYER2 if player == 0 else self.PLAYER1
        if player == self.move % 2:
            # black is 1 and black starts, so black only plays on even move numbers
            # if not players turn, return error dict 
            return {'type': 'error', 'player': curr_player_color, 'row': row, 'col': col, 'message': 'Not your turn.'}
        flips = self.find_valid_flips(player, row, col)
        valid_click = len(flips) > 0
        if not valid_click:
            return {'type': 'error', 'player': curr_player_color, 'row': row, 'col': col, 'message': 'Not a valid move.'}
        
        # update game state
        self.grid[row][col] = player 
        to_white = len(flips) + 1 if player == 0 else -len(flips)
        to_black = len(flips) + 1 if player == 1 else -len(flips)
        self.white_score += to_white
        self.black_score += to_black
        self.make_flips(flips)
        return {'type': 'play', 'player': curr_player_color, 'row': row, 'col': col, 
                'message': f'{curr_player_color.capitalize()} made a play at ({row}, {col}).'}


    def find_valid_flips(self, player: int, row: int, col: int):
        white_is_next = self.move % 2 == 1
        check_val = 1 if white_is_next else 0
        curr_val = 1 - check_val
        valid_flips = []
        for dx, dy in self.directions:
            row_check = row + dx 
            col_check = col + dy 
            num_pushed = 0
            while (
                0 <= row_check < self.ROWS
                and 0 <= col_check < self.COLS 
                and self.grid[row_check][col_check] == check_val
            ):
                valid_flips.append([row_check, col_check])
                num_pushed += 1
                row_check += dx 
                col_check += dy 
            if (
                0 <= row_check < self.ROWS
                and 0 <= col_check < self.COLS 
                and self.grid[row_check][col_check] != curr_val
            ):
                for _ in range(num_pushed):
                    valid_flips.pop()
        return valid_flips

    def make_flips(self, flips: list[list[int]]):
        for row, col in flips:
            self.grid[row][col] = 1 - self.grid[row][col]
    
    def check_winner(self) -> str | None:
        if (self.white_score + self.black_score == 64 
            or self.white_score == 0
            or self.black_score == 0):
            if self.white_score > self.black_score:
                return 'white'
            elif self.black_score > self.white_score:
                return 'black'
            else:
                return 'tie'
        else:
            return None
        
    def check_valid_move_possible(self) -> bool:
        white_is_next = self.move % 2 == 1
        check_val = 1 if white_is_next == False else 0
        curr_val = 1 - check_val
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col] != None:
                    # only check empty spaces
                    continue
                for dx, dy in self.directions:
                    new_r, new_c = row + dx, col + dy
                    found_opposite_color = False
                    while (
                        0 <= new_r < self.ROWS
                        and 0 <= new_c < self.COLS
                        and self.grid[new_r][new_c] == check_val
                    ):
                        new_r += dx
                        new_c += dy
                        found_opposite_color = True
                    # now that we've found the end of the opposite color (check_val)
                    if (
                        0 <= new_r < self.ROWS
                        and 0 <= new_c < self.COLS
                        and found_opposite_color
                        and self.grid[new_r][new_c] == curr_val
                    ):
                        return True
        return False
    
    def forfeit_move(self) -> None:
        self.move += 1
