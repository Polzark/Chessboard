from constants import *
import chess
import board
import neopixel
from cali_mux import find_changes, copy_board

class Game:
    def __init__(self, chessboard):
        self.chessboard = chessboard    # updates after every legal move
        self.interimboard = copy_board()  # updates after pick up, put down
        self.game_state = Pickup_State(PieceColour.WHITE, self) # White player first
        self.pixels = neopixel.NeoPixel(board.D18, 8, auto_write=False) # D18 is physical/GPIO.BOARD pin 12
        self.legal_squares = []
        self.from_square = -1
    
    # find all legal moves from a given square
    def find_squares(self, square):
        self.legal_squares = []
        for move in self.chessboard.legal_moves:
            if move.from_square == square:
                self.legal_squares.append(chess.square_name(move.to_square))
        return self.legal_squares
    
    # just calls the state function
    def calc(self, square, incoming_board_data):
        self.game_state.piece_change(square, incoming_board_data)

    # lights up all the given squares
    def lightup_squares(self, squares):
        for square in squares:
            ## convert to row and col index
            row = chess.square_file(square)
            col = chess.square_rank(square)
            if (col == 0):
                self.pixels[row] = (255,0,0)
        self.pixels.show()
    
    # Lights up all lights with the colour red (chatgpt said that double brackets work
    # i believe in it)
    def error_lightup(self):
        self.pixels.fill((0, 255, 0))
        self.pixels.show()
    
    # turn all lights off
    def revert_lights(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()
        self.curr_lights = []

    # just to change state of the game
    def change_state(self, game_state):
        self.game_state = game_state

    def is_legal_square(self, square):
        for sq in self.legal_squares:
            if (chess.parse_square(square) == sq):
                return True
        return False


    
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
        print(f"is colour same:{self.same_colour(changes[0]['square']) } ")
        print(f"is piece removed: {changes[0]['action'] == 'removed'}")
        if self.game.chessboard.color_at(chess.parse_square(changes[0]['square'])) == self.colour and changes[0]['action'] == 'removed':
            squares = self.game.find_squares(chess.parse_square(changes[0]['square']))
            self.game.legal_squares = squares
            self.game.from_square = chess.parse_square(changes[0]['square'])
            self.game.lightup_squares(squares)
            self.game.interimboard = copy_board()
            self.game.change_state(Putdown_State(self.colour, self.game))
        else:
            self.game.change_state(Error_State(self.colour, self.game, self))
            self.game.error_lightup()
            print(f"Panik_DOWN: {self.colour}")
            print(f"piece colour: {self.game.chessboard.color_at(chess.parse_square(changes[0]['square']))}")
            # print(f", Symbol: {self.game.chessboard.piece_at(chess.parse_square(changes[0]['square'])).symbol()}")
        

class Putdown_State(Game_State):
    def __init__(self, colour, game):
        super().__init__(colour, game)
        self.capture = False
        self.capture_square = -1

    def piece_change(self, changes, chessboard):
        # if change is put down, check if chosen square is valid and has not captured already
        if self.game.is_legal_square(changes[0]['square']) and changes[0]['action'] == 'placed' and self.capture == False:
            self.finalise_move(chess.parse_square(changes[0]['square']))
        # if change is a pick up, check if it is a valid pick up
        # 1. the square is part of legal_squares
        # 2. the piece is of the opposite colour
        elif self.game.is_legal_square(changes[0]['square']) and changes[0]['action'] == 'removed' and self.capture == False and not self.same_colour(changes[0]['square']):
            self.capture = True
            self.capture_square = chess.parse_square(changes[0]['square'])
        
        # if change is put down and a piece has been captured already,
        # must make sure the put down square is the same
        elif self.capture_square == chess.parse_square(changes[0]['square']) and changes[0]['action'] == 'placed':
            self.finalise_move(chess.parse_square(changes[0]['square']))
        else:
            self.game.change_state(Error_State(self.colour, self.game, self))
            self.game.error_lightup()
            print(f"Panik_UP: {self.colour}")
            # print(f", Symbol: {self.game.chessboard.piece_at(chess.parse_square(changes[0]['square'])).symbol()}")
    
    def finalise_move(self, to_square):
            self.game.chessboard.push(chess.Move(self.game.from_square, to_square))
            self.game.revert_lights()
            self.game.interimboard = copy_board()
            self.game.from_square = -1
            self.game.change_state(Pickup_State(not self.colour, self.game))
        

class Error_State(Game_State):
    def __init__(self, colour, game, prev_state):
        super().__init__(colour, game)
        self.prev_state = prev_state

    def piece_change(self, changes, chessboard):
        same = find_changes(self.game.interimboard, chessboard)
        if not same:
            self.game.error_lightup()
        else:
            self.game.revert_lights()
            self.game.game_state = self.prev_state
