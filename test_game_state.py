from constants import Constants
from game import Game
from game_state import GameState
from piece import Piece


def test_constructor():
    gs = GameState()
    assert(gs == GameState())


def test_set_initial_square():
    gs = GameState()
    # run method
    gs.set_initial_square()

    # set squares to all empty piece objects
    squares = [[Piece(Constants.EMPTY, -1, -1, [[], []])]
               * Constants.COLUMNS for _ in range(Constants.ROWS)]

    # create black pieces
    black_piece1 = Piece(Constants.BLACK, 0, 1, [[1, -1], [1, 1]])
    black_piece2 = Piece(Constants.BLACK, 0, 3, [[1, -1], [1, 1]])
    black_piece3 = Piece(Constants.BLACK, 0, 5, [[1, -1], [1, 1]])
    black_piece4 = Piece(Constants.BLACK, 0, 7, [[1, -1], [1, 1]])
    black_piece5 = Piece(Constants.BLACK, 1, 0, [[1, -1], [1, 1]])
    black_piece6 = Piece(Constants.BLACK, 1, 2, [[1, -1], [1, 1]])
    black_piece7 = Piece(Constants.BLACK, 1, 4, [[1, -1], [1, 1]])
    black_piece8 = Piece(Constants.BLACK, 1, 6, [[1, -1], [1, 1]])
    black_piece9 = Piece(Constants.BLACK, 2, 1, [[1, -1], [1, 1]])
    black_piece10 = Piece(Constants.BLACK, 2, 3, [[1, -1], [1, 1]])
    black_piece11 = Piece(Constants.BLACK, 2, 5, [[1, -1], [1, 1]])
    black_piece12 = Piece(Constants.BLACK, 2, 7, [[1, -1], [1, 1]])
    # create red pieces
    red_piece1 = Piece(Constants.RED, 7, 0, [[-1, -1], [-1, 1]])
    red_piece2 = Piece(Constants.RED, 7, 2, [[-1, -1], [-1, 1]])
    red_piece3 = Piece(Constants.RED, 7, 4, [[-1, -1], [-1, 1]])
    red_piece4 = Piece(Constants.RED, 7, 6, [[-1, -1], [-1, 1]])
    red_piece5 = Piece(Constants.RED, 6, 1, [[-1, -1], [-1, 1]])
    red_piece6 = Piece(Constants.RED, 6, 3, [[-1, -1], [-1, 1]])
    red_piece7 = Piece(Constants.RED, 6, 5, [[-1, -1], [-1, 1]])
    red_piece8 = Piece(Constants.RED, 6, 7, [[-1, -1], [-1, 1]])
    red_piece9 = Piece(Constants.RED, 5, 0, [[-1, -1], [-1, 1]])
    red_piece10 = Piece(Constants.RED, 5, 2, [[-1, -1], [-1, 1]])
    red_piece11 = Piece(Constants.RED, 5, 4, [[-1, -1], [-1, 1]])
    red_piece12 = Piece(Constants.RED, 5, 6, [[-1, -1], [-1, 1]])
    # add black pieces
    squares[0][1] = black_piece1
    squares[0][3] = black_piece2
    squares[0][5] = black_piece3
    squares[0][7] = black_piece4
    squares[1][0] = black_piece5
    squares[1][2] = black_piece6
    squares[1][4] = black_piece7
    squares[1][6] = black_piece8
    squares[2][1] = black_piece9
    squares[2][3] = black_piece10
    squares[2][5] = black_piece11
    squares[2][7] = black_piece12
    # add red pieces
    squares[7][0] = red_piece1
    squares[7][2] = red_piece2
    squares[7][4] = red_piece3
    squares[7][6] = red_piece4
    squares[6][1] = red_piece5
    squares[6][3] = red_piece6
    squares[6][5] = red_piece7
    squares[6][7] = red_piece8
    squares[5][0] = red_piece9
    squares[5][2] = red_piece10
    squares[5][4] = red_piece11
    squares[5][6] = red_piece12
    # compare nested lists
    assert(gs.squares == squares)
