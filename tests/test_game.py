from ..game import Othello


def generate_grid(n: int, value: None | int = None) -> list[list[int | None]]: 
    return [[value] * n for _ in range(n)]

def test_valid_move_available(): 
    game = Othello()
    assert game.check_valid_move_possible() == True

def test_no_valid_move_available():
    # generate grid full of 1's (black)
    grid = generate_grid(8)
    grid[3][3] = 1
    grid[3][4] = 1
    grid[4][3] = 1
    grid[4][4] = 1
    game = Othello(starting_grid=grid)
    assert game.check_valid_move_possible() == False 

def test_no_winner(): 
    game = Othello()
    assert game.check_winner() == None

def test_white_wins():
    game = Othello()
    game.white_score = 33
    game.black_score = 31
    assert game.check_winner() == 'white'

def test_black_wins():
    game = Othello()
    game.black_score = 33
    game.white_score = 31
    assert game.check_winner() == 'black'

def test_game_tie():
    game = Othello()
    game.white_score = 32
    game.black_score = 32
    assert game.check_winner() == 'tie'

def test_make_move_returns_error_if_not_turn(): 
    game = Othello() # start with default board
    resp = game.make_move(0, 4, 2) # make move at (4, 2), should return error dict since black starts first
    assert resp['type'] == 'error'
    assert resp['message'] == 'Not your turn.'

def test_make_move_error_if_invalid_move():
    game = Othello()
    resp = game.make_move(1, 4, 2)
    assert resp['type'] == 'error'
    assert resp['message'] == 'Not a valid move.'

def test_valid_move_generates_correct_response():
    grid = generate_grid(3)
    grid[1][1] = 0
    grid[1][2] = 1
    grid[2][1] = 1
    grid[2][2] = 0
    game = Othello(starting_grid=grid)
    resp = game.make_move(1, 1, 0)
    assert resp['type'] == 'play'
    assert resp['message'] == 'Black made a play at (1, 0).'

def test_valid_move_updates_grid():
    grid = generate_grid(3)
    grid[1][1] = 0
    grid[1][2] = 1
    grid[2][1] = 1
    grid[2][2] = 0
    game = Othello(starting_grid=grid)
    game.make_move(1, 1, 0)
    assert game.grid == [
        [None, None, None],
        [1, 1, 1],
        [None, 1, 0]
    ]

def test_valid_move_updates_scores():
    grid = generate_grid(3)
    grid[1][1] = 0
    grid[1][2] = 1
    grid[2][1] = 1
    grid[2][2] = 0
    game = Othello(starting_grid=grid)
    game.make_move(1, 1, 0)
    assert game.white_score == 1
    assert game.black_score == 4


