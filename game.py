import random
import turtle
from constants import Constants
from turtle import Turtle, position
from game_state import GameState
from piece import Piece


class Game:
    '''
        Class -- Game
            Draws the checkers board and handles the user clicks as well as
            the AI
        Attributes:
            game_state -- An instance of the GameState object
            player_move -- A potential move object the player is trying to
                carry out
        Methods:
            click_handler -- determines how to handle user clicks
            ai_turn -- moves the AI pieces based on a randomly chosen move
            get_ai_move -- gets a move for the AI to do
            make_move -- updates the board GUI and gamestate with the move
                that was just performed
            get_player_moves -- get the moves for the current player at the
                start of their turn
            get_capture_moves -- when a capture is made, checks to see if that
                piece can make any more captures
            print_moves -- prints out available moves
            get_possible_moves -- when a piece is clicked, checks for its
                possible moves and highlights them on the board GUI
            clear_possible_moves -- clears square highlights
            check_game_over -- checks to see if the game is over
            display_winner -- draws a message on the GUI when there is a winner
            more_capture_moves -- checks to see if there are more capture
                moves after a capture move was made
            change_player -- changes the current player
            get_xy_coordinates -- converts a location to a pixel coordinate
            get_square_position -- converts a pixel to a row/col location
            is_valid_first_click -- confirms valid first click
            check_for_move -- checks the user clicks against all possible
                valid moves
            start_turtle -- creates an instance of Turtle to draw the board
            draw_board -- uses Turtle to draw the squares and pieces on the
                board with the correct color
            draw_square -- draws a square on the board using Turtle
            draw_circle -- draws a circle on the board using Turtle
            draw_king -- draws a crown on a pice that is a king
            draw_move_square -- draws a new square over an old square
            draw_move_piece -- draws a new circle on a square

    '''

    def __init__(self, testing):
        '''
            Constructor -- creates a new instance of Game
            Parameters:
                self -- the current Game object
        '''
        self.game_state = GameState()
        self.player_move = None
        # draw board and get move for black team
        if not testing:
            self.start_turtle()

    def click_handler(self, x, y):
        '''
        Method -- click_handler
            Determines how to handle a user click, tracking the first and
            second click to form a complete move
        Parameters:
            self -- the current Game object
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        '''
        POS_BOUND = 200
        NEG_BOUND = -200
        if x > POS_BOUND or x < NEG_BOUND or y > POS_BOUND or y < NEG_BOUND:
            print(x, y, "is out of bounds")
        else:
            col = self.get_square_position(x)
            row = self.get_square_position(y)
            # piece color at square
            clicked_piece = self.game_state.squares[row][col]

            # check if first click is valid
            if clicked_piece.get_color() != Constants.EMPTY and \
                    self.is_valid_first_click(clicked_piece.get_color()):
                # update click tracker at index 0
                self.game_state.click_tracker[0] = [row, col]
                # use click to draw indicator of which squares are an option
                self.get_possible_moves(clicked_piece)

            # start check to see if clicks make a move
            elif self.check_for_move([self.game_state.click_tracker[0],
                                      [row, col]]):
                # carry out player move
                self.make_move(self.player_move)
                # check to see if more capture moves after first capture move
                if self.more_capture_moves():
                    for jump_move in self.game_state.capture_moves:
                        print("Another jump possible from {} to {}".format(
                            jump_move.get_start(), jump_move.get_end()))
                # no more actions for player to take, change player and
                # check if game over
                else:
                    self.change_player()
                    if not self.check_game_over():
                        self.screen.ontimer(self.ai_turn, 1000)

    def ai_turn(self):
        '''
            Method -- ai_turn
                randomly selects a move for red team and carries it out
            Parameters:
                self -- the current Game object
        '''
        chosen_move = self.get_ai_move()
        # make move with randomly chosen move
        self.make_move(chosen_move)
        # AI check to see if there are additional capture moves
        if self.more_capture_moves():
            for jump_move in self.game_state.capture_moves:
                print("Another jump possible from {} to {}".format(
                    jump_move.get_start(), jump_move.get_end()))
            self.screen.ontimer(self.ai_turn, 1000)
        else:
            self.change_player()
            self.check_game_over()

    def get_ai_move(self):
        '''
            Method -- get_ai_move
                gets a move for the AI to do, helper function for ai_turn
            Parameters:
                self -- the current Game object
            Returns:
                a move object
        '''
        # if move in capture list, pick random move from there
        if len(self.game_state.capture_moves) > 0:
            move = random.choice(self.game_state.capture_moves)
        # else, pick random move from move list
        else:
            move = random.choice(self.game_state.next_moves)
        return move

    def make_move(self, move):
        '''
            Method -- make_move
                updates the board GUI and gamestate with the move that 
                was just performed
            Parameters:
                self -- the current Game object
                move -- a move object to be implemented
        '''
        # draw over highlighted squares
        self.clear_possible_moves()
        # get row/col of piece to be moved
        row = move.get_start()[0]
        col = move.get_start()[1]
        # get row/col of end location for moving piece
        new_row = move.get_end()[0]
        new_col = move.get_end()[1]
        # get piece object
        piece_to_move = self.game_state.squares[row][col]
        # move piece object to new square in gamestate
        self.game_state.squares[new_row][new_col] = piece_to_move
        # update piece object with it's new row/col
        piece_to_move.set_row(new_row)
        piece_to_move.set_col(new_col)

        # draw over old square
        self.draw_move_square(move.get_start())
        # update game state for old square to empty
        self.game_state.squares[row][col] = \
            Piece(Constants.EMPTY, -1, -1, [[], []])

        # draw piece at new square
        self.draw_move_piece(move.get_end(), piece_to_move)

        if move.is_capture():
            # draw over captured piece
            self.draw_move_square(move.get_captured_square())
            # update game state for captured square to empty
            self.game_state.squares[move.get_captured_row(
            )][move.get_captured_col()] = \
                Piece(Constants.EMPTY, -1, -1, [[], []])

            # clear move list to allow for checking of new captures
            self.game_state.reset_move_lists()
            # check piece that moved for any additional capture moves
            self.get_capture_moves(piece_to_move)

    def get_player_moves(self, player):
        '''
            Method -- get_player_moves
                get the moves for the current player at the start of their
                turn and prints out what they can do to the console
            Parameters:
                self -- the current Game object
                player -- a string representing the color of the current player
        '''
        for row in self.game_state.squares:
            for square in row:
                if square.get_color() == player:
                    square.get_moves(self.game_state)
        for move in self.game_state.next_moves:
            if move.is_capture():
                self.game_state.capture_moves.append(move)
            if len(self.game_state.capture_moves) > 0:
                self.game_state.next_moves = self.game_state.capture_moves
        self.print_moves()

    def get_capture_moves(self, piece):
        '''
            Method -- get_capture_moves
                when a capture is made, checks to see if that piece can make
                any more captures
            Parameters:
                self -- the current Game object
                piece -- Piece object used to check for any additional capture
                moves from its new location
        '''
        piece.get_moves(self.game_state)
        for move in self.game_state.next_moves:
            if move.is_capture():
                self.game_state.capture_moves.append(move)
                self.game_state.next_moves = self.game_state.capture_moves

    def print_moves(self):
        '''
            Method -- print_moves
                prints out available moves for the current player
            Parameters:
                self -- the current Game object
        '''
        for move in self.game_state.next_moves:
            print("{} can move from: {} to: {} Capture: {}".format(
                self.game_state.get_player(),
                move.start, move.end, move.capture))

    def get_possible_moves(self, piece):
        '''
            Method -- get_possible_moves
                when a piece is clicked, checks for its possible moves and
                highlights them on the board GUI
            Parameters:
                self -- the current Game object
                piece -- the Piece object to check for possible moves
        '''
        self.clear_possible_moves()
        for move in self.game_state.next_moves:
            if [piece.get_row(), piece.get_col()] == move.get_start():
                self.game_state.possible_moves.append(move)
                possible_y = self.get_xy_coordinates(move.get_end()[0])
                possible_x = self.get_xy_coordinates(move.get_end()[1])
                self.draw_square(self.pen, Constants.SQUARE,
                                 Constants.PIECE_COLORS[1],
                                 Constants.SQUARE_COLORS[0],
                                 possible_x, possible_y)

    def clear_possible_moves(self):
        '''
            Method -- clear_possible_moves
                clears square highlights once a new piece is clicked or a move
                is made.
            Parameters:
                self -- the current Game object
        '''
        if len(self.game_state.possible_moves) > 0:
            for move in self.game_state.possible_moves:
                reset_y = self.get_xy_coordinates(move.get_end()[0])
                reset_x = self.get_xy_coordinates(move.get_end()[1])
                self.draw_square(self.pen, Constants.SQUARE,
                                 Constants.SQUARE_COLORS[2],
                                 Constants.SQUARE_COLORS[0],
                                 reset_x, reset_y)
            self.game_state.possible_moves.clear()

    def check_game_over(self):
        '''
            Method -- check_game_over
                checks to see if the game is over by looking at the length
                of the move list for the current player. Draws a message
                if game is over on the GUI
            Parameters:
                self -- the current Game object
            Returns:
                True if team has no more moves, false otherwise
        '''
        if len(self.game_state.next_moves) == 0:
            self.game_state.set_player()
            self.display_winner(self.game_state.get_player())
            return True

    def display_winner(self, win_color):
        '''
            Method -- display_winner
                draws a message on the GUI when there is a winner, helper
                method for check_game_over
            Parameters:
                self -- the current Game object
                win_color -- a string representing the color of the winning team
        '''
        if win_color == Constants.PIECE_COLORS[0]:
            text = "Game Over\n\nYou Win!"
        else:
            text = "Game Over\n\nYou Lose!"
        style = ('Courier', 50, 'bold')
        self.pen.color("green")
        self.pen.setposition(0, 0)
        self.pen.write(text, font=style, align='center')

    def more_capture_moves(self):
        '''
            Method -- more_capture_moves
                checks to see if there are more capture moves after a capture
                move was made, called by AI and click handler
            Parameters:
                self -- the current Game object
            Returns:
                True if there are more capture moves, False otherwise
        '''
        return len(self.game_state.capture_moves) > 0

    def change_player(self):
        '''
            Method -- change_player
                runs at the end of the turn to start the player change
            Parameters:
                self -- the current Game object
        '''
        # reset list and update current player to end turn
        self.game_state.end_player_turn()
        # get moves for next player
        self.get_player_moves(self.game_state.get_player())

    def get_xy_coordinates(self, location):
        '''
            Method -- get_xy_coordinates -- converts a col and row to x and y

            Parameters:
                self -- the current Game object
                location -- the row or col location of the square
            Returns:
                the pixel coordinate of the location
        '''
        return (location - 4) * 50

    def get_square_position(self, pixel):
        '''
            Method -- get_square_position
                converts a pixel to a row/col location
            Parameters:
                self -- the current Game object
                pixel -- the x or y coordinate of where the user clicked
            Returns:
                the location of where the user clicked (row or col)
        '''
        return int(pixel // 50 + 4)

    def is_valid_first_click(self, click):
        '''
            Method -- is_valid_first_click
                confirms the first click by the user is on one of their pieces
            Parameters:
                self -- the current Game object
                click -- a string representing the color of the clicked piece
            Returns:
                True if piece and player color match, False otherwise
        '''
        return click == self.game_state.get_player()

    def check_for_move(self, clicks):
        '''
            Method -- check_for_move
                checks the user clicks against all possible valid moves
            Parameters:
                self -- the current Game object
                clicks -- a nested list of the users valid first click and
                second click
            Returns:
                True if the clicks match a move object in the list, False
                otherwise
        '''
        for move in self.game_state.next_moves:
            if clicks == [move.get_start(), move.get_end()]:
                self.player_move = move
                return True

    # board drawing methods

    def start_turtle(self):
        '''
            Method -- start_turtle
                creates an instance of Turtle to draw the board
            Parameters:
                self -- the current Game object
        '''
        turtle.setup(Constants.WINDOW_SIZE, Constants.WINDOW_SIZE)
        # Set the drawing canvas size. The should be actual board size
        turtle.screensize(Constants.BOARD_SIZE, Constants.BOARD_SIZE)
        turtle.bgcolor("white")
        turtle.tracer(0, 0)
        # create pen to draw
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.pen.hideturtle()

        # Draw the game board
        self.draw_board()
        self.get_player_moves(self.game_state.get_player())

        # Click handling
        self.screen = turtle.Screen()
        # This will call call the click_handler function when a click occurs
        self.screen.onclick(self.click_handler)
        turtle.done()

    def draw_board(self):
        '''
            Method -- draw_board
                uses Turtle to draw the squares and pieces on the board with
                the correct color and location
            Parameters:
                self -- the current Game object
        '''
        corner = -Constants.BOARD_SIZE / 2
        self.pen.setposition(corner, corner)
        for row in range(Constants.ROWS):
            for col in range(Constants.COLUMNS):
                if col % 2 != row % 2:
                    self.draw_square(self.pen, Constants.SQUARE,
                                     Constants.SQUARE_COLORS[2],
                                     Constants.SQUARE_COLORS[0],
                                     corner + (Constants.SQUARE * row),
                                     corner + (Constants.SQUARE * col))
                    if col < Constants.BLACK_ROWS:
                        self.draw_circle(
                            self.pen, Constants.PIECE_SIZE,
                            Constants.PIECE_COLORS[0],
                            corner + (Constants.SQUARE * row) +
                            Constants.PIECE_SIZE,
                            corner + (Constants.SQUARE * col))
                    elif col > Constants.RED_ROWS:
                        self.draw_circle(
                            self.pen, Constants.PIECE_SIZE,
                            Constants.PIECE_COLORS[1],
                            corner + (Constants.SQUARE * row) +
                            Constants.PIECE_SIZE,
                            corner + (Constants.SQUARE * col))
                else:
                    self.draw_square(
                        self.pen, Constants.SQUARE,
                        Constants.SQUARE_COLORS[2],
                        Constants.SQUARE_COLORS[1],
                        corner + (Constants.SQUARE * row),
                        corner + (Constants.SQUARE * col))

    def draw_square(self, a_turtle, size, outline, fill, x, y):
        '''
            Method -- draw_square
                Draw a square on the board
            Parameters:
                a_turtle -- an instance of Turtle
                size -- the length of each side of the square
                outline -- color of the square outline
                fill -- color of the squares fill
                x -- x coordinate to start
                y -- y coordinate to start
        '''
        RIGHT_ANGLE = 90

        a_turtle.setposition(x, y)
        a_turtle.pendown()
        a_turtle.color(outline, fill)
        a_turtle.begin_fill()
        for i in range(4):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_circle(self, a_turtle, size, color, x, y):
        '''
            Method -- draw_circle
                draws a circle on the board
            Parameters:
                a_turtle -- an instance of Turtle
                size -- the radius of the circle
                color -- the color of the circle
                x -- x coordinate to start
                y -- y coordinate to start
            Returns:
                Nothing. Draws a circle in the graphics window.
        '''
        a_turtle.setposition(x, y)
        a_turtle.pendown()
        a_turtle.color(color)
        a_turtle.begin_fill()
        a_turtle.circle(size)
        a_turtle.end_fill()
        a_turtle.penup()

    def draw_king(self, a_turtle, outline, x, y):
        '''
            Method -- draw_king
                draws a crown on a pice that is a king
            Parameters:
                self -- the current Game object
                a_turtle -- an instance of Turtle
                outline -- color of the square outline
                x -- x coordinate to start
                y -- y coordinate to start
        '''
        RIGHT_ANGLE = 90
        BOTTOM_CROWN = 21
        SIDE_CROWN = 5
        CROWN_PEAK = 10
        CROWN_TOP_ANGLE = 70
        CROWN_BOTTOM_ANGLE = 140

        a_turtle.setposition(x + 14, y + 23)
        a_turtle.pendown()
        a_turtle.color(outline)
        for i in range(3):
            a_turtle.left(CROWN_TOP_ANGLE)
            a_turtle.forward(CROWN_PEAK)
            a_turtle.right(CROWN_BOTTOM_ANGLE)
            a_turtle.forward(CROWN_PEAK)
            a_turtle.left(CROWN_TOP_ANGLE)
        a_turtle.setheading(270)
        a_turtle.forward(SIDE_CROWN)
        a_turtle.right(RIGHT_ANGLE)
        a_turtle.forward(BOTTOM_CROWN)
        a_turtle.right(RIGHT_ANGLE)
        a_turtle.forward(SIDE_CROWN)
        a_turtle.setheading(0)
        a_turtle.penup()

    def draw_move_square(self, row_col):
        '''
            Method -- draw_move_square
                draws over a square when a move is made
            Parameters:
                self -- the current Game object
                row_col -- a list with two ints indicating a row and column
        '''
        x = self.get_xy_coordinates(row_col[1])
        y = self.get_xy_coordinates(row_col[0])
        self.draw_square(self.pen, Constants.SQUARE,
                         Constants.SQUARE_COLORS[2],
                         Constants.SQUARE_COLORS[0], x, y)

    def draw_move_piece(self, row_col, piece):
        '''
            Method -- draw_move_piece
                draws a new piece at the square it moved to
            Parameters:
                self -- the current Game object
                row_col -- a list with two ints indicating a row and column
                piece -- a Piece object
        '''
        x = self.get_xy_coordinates(row_col[1])
        y = self.get_xy_coordinates(row_col[0])
        self.draw_circle(self.pen, Constants.SQUARE / 2,
                         self.game_state.get_player(), x + 25, y)
        # if king piece, draw crown on piece
        if piece.is_king == True:
            self.draw_king(self.pen, Constants.PIECE_COLORS[2], x, y)
