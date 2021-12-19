from piece import Piece
from constants import Constants


class GameState:
    '''
        Class -- GameState
            Maintains the state of the playing board
        Attributes:
            squares -- a nested list containing the state of the board,
                indicating which square is empty and which square has a checker
            current_player -- the current player of the game
            click_tracker -- list to track each valid first and second click
                by the player to make a move
            next_moves -- a list that propagates with the players available
                moves at the start of their turn
            capture_moves -- a list of the players possible capture moves,
                propagates before and during a plyers turn
            possible_moves -- a list to track the possible moves for the
                piece that the player clicks on during their turn. used to 
                highlight those squares

        Methods:
            get_player -- gets the color of the current player up to move
            set_player -- changes the current player value
            set_initial_square -- initializes the nested list
            set_color_square -- iterates through the nested list, creating
                checker piece objects and placing them at the appropriate index
            reset_move_lists -- resets all move tracking lists after a move
            end_player_turn -- resets move lists and changes current player
    '''

    def __init__(self):
        '''
            Constructor -- creates a new instance of GameState
            Parameters:
                self -- the current GameState object
        '''

        self.squares = []
        self.set_initial_square()
        self.current_player = Constants.BLACK
        self.click_tracker = [[-1, -1], [-1, -1]]
        self.next_moves = []
        self.capture_moves = []
        self.possible_moves = []

    def get_player(self):
        '''
            Method -- get_player
                gets the current player
            Parameters:
                self -- the current GameState object
            Returns:
                A string indicating the color of the current player
        '''
        return self.current_player

    def set_player(self):
        '''
            Method -- set_player
                Changes the current player
            Parameters:
                self -- the current GameState object
        '''
        if self.current_player == Constants.BLACK:
            self.current_player = Constants.RED
        else:
            self.current_player = Constants.BLACK

    def set_initial_square(self):
        '''
            Method -- set_initial_square
                initializes the nested list to all empty objects
            Parameters:
                self -- the current GameState object
        '''
        self.squares = [[Piece(Constants.EMPTY, -1, -1, [[], []])]
                        * Constants.COLUMNS for _ in range(Constants.ROWS)]
        self.set_color_square()

    def set_color_square(self):
        '''
            Method -- set_color_square
                iterates through the nested list squares, checker piece 
                objects and placing them at the appropriate index
            Parameters:
                self -- the current GameState object
        '''
        BLACK_ROWS = 3
        RED_ROWS = 4
        for row in range(Constants.COLUMNS):
            for col in range(Constants.ROWS):
                if col % 2 != row % 2:
                    if row < BLACK_ROWS:
                        self.squares[row][col] = Piece(
                            Constants.BLACK, row, col, [[1, -1], [1, 1]])
                    if row > RED_ROWS:
                        self.squares[row][col] = Piece(
                            Constants.RED, row, col, [[-1, -1], [-1, 1]])

    def reset_move_lists(self):
        '''
            Method -- reset_move_lists
                sets lists back to initial state after player turn
            Parameters:
                self -- the current GameState object
        '''
        self.click_tracker = [[-1, -1], [-1, -1]]
        self.next_moves = []
        self.capture_moves = []
        self.possible_moves = []

    def end_player_turn(self):
        '''
            Method -- end_player_turn
                resets lists and changes player
            Parameters:
                self -- the current GameState object
        '''
        self.reset_move_lists()
        self.set_player()

    def __eq__(self, other):
        return self.squares == other.squares and \
            self.current_player == other.current_player and \
            self.click_tracker == other.click_tracker and \
            self.next_moves == other.next_moves and \
            self.capture_moves == other.capture_moves and \
            self.possible_moves == other.possible_moves
