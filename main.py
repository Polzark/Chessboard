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
chess_board = chess.Board()

chess_init = [[0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [1,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]

previous_board = chess_init
game = Game(chess_board)

try:
    while not chess_board.is_game_over():
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
