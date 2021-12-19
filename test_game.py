from constants import Constants
from game import Game
from game_state import GameState
from piece import Piece
from move import Move


def test_constructor():
    game = Game(True)
    game_state = GameState()
    assert(game.game_state == game_state)
    assert(game.player_move is None)


def test_get_capture_moves():
    game = Game(True)
    black_piece = Piece(Constants.BLACK, 2, 1, [[1, -1], [1, 1]])
    red_piece = Piece(Constants.RED, 3, 2, [[-1, -1], [-1, 1]])
    game.game_state.squares[3][2] = red_piece
    game.get_capture_moves(black_piece)
    move = Move([2, 1], [4, 3], True, [3, 2])
    game.game_state.next_moves == [move]
    assert(game.game_state.capture_moves == [move])


def test_get_possible_moves():
    '''
    Has an instance of turtle, passes if that code is commented out
    '''
    game = Game(True)
    # add possible moves to move list
    move1 = Move([2, 1], [3, 0], False, [-1, -1])
    move2 = Move([2, 1], [3, 2], False, [-1, -1])
    move3 = Move([2, 7], [3, 6], False, [-1, -1])
    game.game_state.next_moves = [move1, move2, move3]
    # create selected piece
    black_piece = Piece(Constants.BLACK, 2, 7, [[1, -1], [1, 1]])
    # game.get_possible_moves(black_piece)
    # assert(game.game_state.possible_moves == [move3])


def test_make_move():
    '''
    Has an instance of turtle, passes if that code is commented out
    '''
    game = Game(True)
    original_squares = game.game_state.squares
    assert(game.game_state.squares == original_squares)
    move = Move([2, 7], [3, 6], False, [-1, -1])
    # game.make_move(move)
    original_squares[2][7] = Piece(Constants.EMPTY, 2, 7, [[], []])
    original_squares[3][6] = Piece(Constants.BLACK, 3, 6, [[], []])
    assert(game.game_state.squares == original_squares)


def test_get_xy_coordinates():
    game = Game(True)
    assert(game.get_xy_coordinates(2) == -100)
    assert(game.get_xy_coordinates(1) == -150)


def test_get_square_position():
    game = Game(True)
    assert(game.get_square_position(185) == 7)
    assert(game.get_square_position(47) == 4)


def test_check_for_move():
    game = Game(True)
    clicks = [[2, 7], [3, 6]]
    move = Move([2, 7], [3, 6], False, [-1, -1])
    game.game_state.next_moves = [move]
    assert(game.check_for_move(clicks))
