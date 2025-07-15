from constants import *
import chess
import board
import neopixel

class Game:
    def __init__(self, chessboard):
        self.chessboard = chessboard
        self.state = Pickup_State(PieceColour.WHITE)
        self.game_state = Pickup_State(PieceColour.WHITE, self)
        self.curr_lights = []
        self.pixels = neopixel.NeoPixel(board.D18, 8)

    def get_legal_moves(self):
        return self.board.legal_moves
    
    def find_squares(self, legal_moves, square):
        squares = []
        for move in legal_moves:
            if move.from_square == square:
                squares.append(chess.square_name(move.to_square))
        return squares
    
    def calc(self, square):
        self.game_state.piece_change(square)

    def lightup_squares(self, squares):
        for square in squares:
            ## convert to row and col index
            row = chess.square_file(square)
            ## don't do col index cuz we only have one column lmao
            self.pixels[row] = neopixel.fill(255,0,0)
        self.curr_lights.append(squares)

    
class Game_State:
    def __init__(self, colour, game):
        self.colour = colour
        self.game = game

    def same_colour(self, square):
        index = chess.parse_square(square)
        colour = self.game.board.color_at(index)
        return colour == self.colour

    def piece_change(self, square):
        pass

class Pickup_State(Game_State):
    def piece_change(self, changes):
        if self.same_colour(changes[0]['square']) and changes[0]['action'] == 'removed':
            squares = self.game.find_squares(self.game.get_legal_moves(), chess.parse_square(changes[0]['square']))
            self.game.lightup_squares(squares)
        else:
            print("Error")
        

class Putdown_State(Game_State):
    def piece_change(self, square):
        self.game.board