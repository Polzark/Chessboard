from constants import *

class Piece:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
    
    def get_type(self):
        return self.name

class Pawn(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.PAWN, colour)

class Knight(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.KNIGHT, colour)

class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.BISHOP, colour)

class Rook(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.ROOK, colour)

class Queen(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.QUEEN, colour)

class King(Piece):
    def __init__(self, colour):
        super().__init__(self, PieceType.KING, colour)