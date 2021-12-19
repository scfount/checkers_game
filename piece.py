from move import Move
from constants import Constants


class Piece:
    '''
        Class -- Piece
            Represents a checkers piece on the board
        Attributes:
            color -- string indicating the team it is on
            size -- an int indicating the diameter of the piece
            row -- an int indicating what row the piece is on
            col -- an int indicating what col the piece is on
            directions -- a list of integers indicating what directions
                the piece can move
            is_king -- a boolean indicating if the piece is a king or not
        Methods:
        get_color -- returns the color of the Piece
        get_opposite_color -- gets the color of the opposite team
        get_size -- returns the size of the piece object
        get_row -- returns the row the piece is on
        get_col -- returns the column the piece is on
        set_row -- sets the row that the piece is now at
        set_col -- sets the column the piece is now at
        set_king -- if piece is at certain location, set it to be a king
            piece and update the directions in can move
        get_directions -- returns the a list of the directions the piece
            can move
        get_moves -- checks the GameState against the piece directions
            to see if a move is possible
    '''

    def __init__(self, color, row, col, directions):
        '''
            Constructor -- creates a new instance of Piece
            Parameters:
                self -- the current Piece object
                color -- string indicating the team it is on
                row -- an int indicating what row the piece is on
                col -- an int indicating what col the piece is on
                directions -- a list of integers indicating what directions 
                the piece can move
        '''
        self.color = color
        self.row = row
        self.col = col
        self.directions = directions
        self.is_king = False

    def get_color(self):
        '''
            Method -- get_color
                gets the color of the Piece object
            Parameters:
                self -- the current GameState object
            Returns:
                A string indicating the color
        '''
        return self.color

    def get_opposite_color(self):
        '''
            Method -- get_opposite_color
                gets the color of the opposite team
            Parameters:
                self -- the current GameState object
            Returns:
                a string representing the color of the opposite team
        '''
        if self.get_color() == Constants.BLACK:
            return Constants.RED
        else:
            return Constants.BLACK

    def get_row(self):
        '''
            Method -- get_row
                the row the piece in on
            Parameters:
                self -- the current GameState object
            Returns:
                an int, the row the piece is on
        '''
        return self.row

    def get_col(self):
        '''
            Method -- get_col
            the column the piece is on
            Parameters:
                self -- the current GameState object
            Returns:
                an int, the column the piece is on
        '''
        return self.col

    def set_row(self, row):
        '''
            Method -- set_row
                sets the row that the Piece is at, if row is a king row,
                set the king value to True
            Parameters:
                self -- the current GameState object
        '''
        self.set_king(row)
        self.row = row

    def set_col(self, col):
        '''
            Method -- set_col
                set the column of the piece on the board
            Parameters:
                self -- the current GameState object
        '''
        self.col = col

    def set_king(self, row):
        '''
            Method -- set_king
                if piece is at certain location, set it to be a king piece
                and update the directions in can move
            Parameters:
                self -- the current GameState object
                row -- int, the row the piece is at
        '''
        if row == Constants.BOTTOM_ROW and self.color == Constants.RED \
                or row == Constants.TOP_ROW and self.color == Constants.BLACK:
            self.is_king = True
            self.directions = [[-1, -1], [-1, 1], [1, -1], [1, 1]]

    def get_directions(self):
        '''
            Method -- get_directions
                returns a nested list of the directions the piece can move
            Parameters:
                self -- the current GameState object
            Returns:
                A nested of list of row/col directions the piece can move
        '''
        return self.directions

    def get_moves(self, game_state):
        '''
            Method -- get_moves
                checks the GameState against the piece directions to see if a
                move is possible. If so, create a new Move object and add
                it to a moves list

            Parameters:
                self -- the current GameState object
                game_state -- the current state of the pieces on the board
        '''
        for direction in self.directions:
            move_row = self.get_row() + direction[0]
            move_col = self.get_col() + direction[1]
            try:
                if game_state.squares[move_row][move_col].get_color() == \
                        Constants.EMPTY and move_row > -1 and move_col > -1:
                    this_move = Move([self.get_row(), self.get_col()],
                                     [move_row, move_col], False, [-1, -1])
                    game_state.next_moves.append(this_move)
                elif game_state.squares[move_row][move_col].get_color() != \
                    Constants.EMPTY and \
                    game_state.squares[move_row][move_col].get_color() == \
                        self.get_opposite_color():
                    jump_row = move_row + direction[0]
                    jump_col = move_col + direction[1]
                    try:
                        if game_state.squares[jump_row][jump_col].get_color() \
                            == Constants.EMPTY and jump_row > -1 and \
                                jump_col > -1:
                            this_move = Move([self.get_row(), self.get_col()],
                                             [jump_row, jump_col], True,
                                             [move_row, move_col])
                            game_state.next_moves.insert(0, this_move)
                    except IndexError:
                        pass

            except IndexError:
                pass

    def __str__(self):
        return "{} Row: {} col: {} king: {}".format(
            self.color, self.row, self.col, self.is_king)

    def __eq__(self, other):
        return self.color == other.color and \
            self.row == other.row and \
            self.col == other.col and \
            self.directions == other.directions and \
            self.is_king == other.is_king
