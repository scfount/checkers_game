from constants import Constants
from game import Game
from piece import Piece
from move import Move


def test_constructor():
    black_piece1 = Piece(Constants.BLACK, 0, 1, [[1, -1], [1, 1]])
    black_piece2 = Piece(Constants.BLACK, 0, 1, [[1, -1], [1, 1]])
    red_piece1 = Piece(Constants.RED, 7, 0, [[-1, -1], [-1, 1]])
    red_piece2 = Piece(Constants.RED, 7, 0, [[-1, -1], [-1, 1]])
    assert(red_piece1 == red_piece2)
    assert(not red_piece1 == black_piece1)
    assert(black_piece1 == black_piece2)


def test_get_moves():
    game = Game(True)
    piece = Piece("Black", 2, 1, [[1, -1], [1, 1]])
    # initial state
    assert(game.game_state.next_moves == [])
    piece.get_moves(game.game_state)
    move1 = Move([2, 1], [3, 0], False, [-1, -1])
    move2 = Move([2, 1], [3, 2], False, [-1, -1])
    # end state
    assert(game.game_state.next_moves == [move1, move2])
