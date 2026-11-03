#!/user/bin/env python3

import numpy as np
from constants import * 
import chess
from cali_mux import chessboard as incoming_board_data, copy_board, current_readings, display_chessboard, find_changes
import RPi.GPIO as GPIO
import time
from Game import *

# Create start positions
Start = [[0 for _ in range(COLS)] for _ in range(ROWS)]
Prev = [[0 for _ in range(COLS)] for _ in range(ROWS)]
print(Start)

# wait for all pieces to be placed


# Start game
# chess_board = chess.Board()

# chess_init = [[0,0,0,0,0,0,0,0], [1,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [1,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

chess_board = chess.Board(None)

# Place a white rook at a8
chess_board.set_piece_at(chess.B8, chess.Piece(chess.PAWN, chess.WHITE))
chess_board.set_piece_at(chess.A7, chess.Piece(chess.ROOK, chess.WHITE))
chess_board.set_piece_at(chess.D5, chess.Piece(chess.QUEEN, chess.BLACK))

print("Waiting for a magnet at a8...")

while True:
    current_readings()

    if incoming_board_data[0][0] == 1 and incoming_board_data[3][3] == 1:
        print("Magnet detected at a8! Starting game.")
        break

    time.sleep(0.5)


# previous_board = chess_init
previous_board = copy_board()
game = Game(chess_board)

try:
    # while not chess_board.is_game_over():
    while True:
        current_readings()

        # Check for changes
        changes = find_changes(incoming_board_data, previous_board)
        if changes:
            print(f"\nDetected {len(changes)} change(s):")
            for change in changes:
                print(f"  {change['square']}: piece {change['action']}")
            game.calc(changes, incoming_board_data)
        
        display_chessboard()
        previous_board = copy_board()
        
        time.sleep(1)  # Slightly longer delay for chess moves

except KeyboardInterrupt:
    print("\nI'm dyinggg...")
    pixels = neopixel.NeoPixel(board.D18, 8, auto_write=False)
    pixels.fill((0,0,0))
    pixels.show()
    GPIO.cleanup()
