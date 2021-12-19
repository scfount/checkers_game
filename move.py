class Move:
    '''
        Class -- Move
            Represents a possible move that can be made
        Attributes:
            start -- a list of the row/col int values of the start of the move
            end -- a list of the row/col int values of the end of the move
            capture -- a boolean indicating if the move is a capturing move
                or not
            captured_square -- the row/col int values of the square that has
                a piece getting captured.
        Methods:
            get_start -- returns the row/col list of the start of the move
            get_end -- returns the row/col list of the end of the move
            is_capture -- returns if the move is a capture or not
            get_captured_square -- returns the row/col list of the square
                that can be captured
            get_captured_row -- returns the row value of the captured square
            get_captured_col -- returns the col value of the captured square

    '''

    def __init__(self, start, end, capture, captured_square):
        '''
            Constructor -- creates a new instance of Move
            Parameters:
                self -- the current Move object
                start -- a list of the row/col int values of the start of the
                    move
                end -- a list of the row/col int values of the end of the move
                capture -- a boolean indicating if the move is a capturing move
                or not
                captured_square -- the row/col int values of the square that
                has a piece getting captured.

        '''
        self.start = start
        self.end = end
        self.capture = capture
        self.captured_square = captured_square

    def get_start(self):
        '''
            Method -- get_start
                the row/col list of the start of the move
            Parameters:
                self -- the current GameState object
            Returns:
                the row/col list of the start of the move
        '''
        return self.start

    def get_end(self):
        '''
            Method -- get_end
                the row/col list of the end of the move
            Parameters:
                self -- the current GameState object
            Returns:
                the row/col list of the end of the move
        '''
        return self.end

    def is_capture(self):
        '''
            Method -- is_capture
                if the move is a capture or not
            Parameters:
                self -- the current GameState object
            Returns:
                True if the move is a capture, False otherwise
        '''
        return self.capture

    def get_captured_square(self):
        '''
            Method -- get_captured_square
                the row/col list of the square that can be captured
            Parameters:
                self -- the current GameState object
            Returns:
                the row/col list of the square that can be captured
        '''
        return self.captured_square

    def get_captured_row(self):
        '''
            Method -- get_captured_row
                the row value of the captured square
            Parameters:
                self -- the current GameState object
            Returns:
            the row value of the captured square
        '''
        return self.captured_square[0]

    def get_captured_col(self):
        '''
            Method -- get_captured_col
                the col value of the captured square
            Parameters:
                self -- the current GameState object
            Returns:
                the col value of the captured square
        '''
        return self.captured_square[1]

    def __str__(self):
        return "start: {}, end: {}, capture: {}".format(
            self.start, self.end, self.capture)

    def __eq__(self, other):
        return self.start == other.start and \
            self.end == other.end and \
            self.capture == other.capture and \
            self.captured_square == other.captured_square
