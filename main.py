import numpy as np
from constants import * 
import chess
from cali_mux import *
from cali_mux import chessboard as incoming_board_data
from Game import *

# Create start positions
Start = [[0 for _ in range(COLS)] for _ in range(ROWS)]
Prev = [[0 for _ in range(COLS)] for _ in range(ROWS)]
print(Start)

# wait for all pieces to be placed


# Start game
chessboard = chess.Board()
previous_board = copy_board()
game = Game(chessboard)

try:
    while not chessboard.is_game_over():
        current_readings()

        # Check for changes
        changes = find_changes(incoming_board_data, previous_board)
        if changes:
            print(f"\nDetected {len(changes)} change(s):")
            for change in changes:
                print(f"  {change['square']}: piece {change['action']}")
            game.calc(changes, chessboard)
        
        display_chessboard()
        previous_board = copy_board()
        
        time.sleep(0.5)  # Slightly longer delay for chess moves

except KeyboardInterrupt:
    print("\nI'm dyinggg...")
