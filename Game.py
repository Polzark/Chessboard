from constants import *
import chess
import board
import neopixel

class Game:
    def __init__(self, chessboard):
        self.chessboard = chessboard    # updates after every legal move
        self.interimboard = chessboard  # updates after pick up, put down
        self.game_state = Pickup_State(PieceColour.WHITE, self) # White player first
        self.curr_lights = []           # current lights that are on to show possible moves
        self.pixels = neopixel.NeoPixel(board.D18, 8)
    
    # find all legal moves from a given square
    def find_squares(self, square):
        squares = []
        for move in self.chessboard.legal_moves:
            if move.from_square == square:
                squares.append(chess.square_name(move.to_square))
        return squares
    
    # just calls the state function
    def calc(self, square, chessboard):
        self.game_state.piece_change(square)

    # lights up all the given squares and adds them to curr_light
    def lightup_squares(self, squares):
        for square in squares:
            ## convert to row and col index
            row = chess.square_file(square)
            col = chess.square_rank(square)
            if (col == 0):
                self.pixels[row] = neopixel.fill(255,0,0)
                self.curr_lights.append(squares)
    
    # lights up all squares on the chessboard for error stuff, could merge with lightup_squares
    def error_lightup(self):
        for row in range(ROWS):
            self.pixels[row] = neopixel.fill(0,255,0)

    # just to change state of the game
    def change_state(self, game_state):
        self.game_state = game_state

    
class Game_State:
    def __init__(self, colour, game):
        self.colour = colour
        self.game = game

    def same_colour(self, square):
        index = chess.parse_square(square)
        colour = self.game.chessboard.color_at(index)
        return colour == self.colour

    def piece_change(self, changes, chessboard):
        pass

class Pickup_State(Game_State):
    def piece_change(self, changes, chessboard):
        if self.same_colour(changes[0]['square']) and changes[0]['action'] == 'removed':
            squares = self.game.find_squares(chess.parse_square(changes[0]['square']))
            self.game.lightup_squares(squares)
            self.game.change_state(Putdown_State(self.colour, self.game))
        else:
            self.game.change_state(Error_State(self.colour, self.game, self))
            self.game.error_lightup()
        

class Putdown_State(Game_State):
    def piece_change(self, changes, chessboard):
        self.game.chessboard

class Error_State(Game_State):
    def __init__(self, colour, game, prev_state):
        super().__init__(colour, game)
        self.prev_state = prev_state

    def piece_change(self, changes, chessboard):
        # ah this very sus lmao
        