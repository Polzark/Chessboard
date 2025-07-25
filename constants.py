from enum import Enum

#Board Dimensions
ROWS = 8
COLS = 1

#Piece types
class PieceType(Enum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class PieceColour(Enum):
    WHITE = True
    BLACK = False