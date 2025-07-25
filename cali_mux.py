import time
import datetime
import RPi.GPIO as GPIO
import chess

###############################################################################
######################### --- Documentation --- ###############################
###############################################################################
#
# RPi.GPIO module: 
# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
#
# Inspired by: 
# https://forums.raspberrypi.com/viewtopic.php?t=267959
#
# CHESSBOARD 2D ARRAY BRANCH
# Enhanced version with 2D array representation for easier chess logic
#
###############################################################################

###############################################################################
###################### --- Initial Setup Stuff --- ############################
###############################################################################

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

# Comments are for GPIO.BOARD
S0_PIN = 17 # 11
S1_PIN = 27 # 13
S2_PIN = 22 # 15
SIG_PIN = 24 # 18
GPIO.setup(S0_PIN, GPIO.OUT) # s0
GPIO.setup(S1_PIN, GPIO.OUT) # s1
GPIO.setup(S2_PIN, GPIO.OUT) # s2
GPIO.setup(SIG_PIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #Signal Input

s0 = [0,1,0,1,0,1,0,1] # s0 values
s1 = [0,0,1,1,0,0,1,1] # s1 values
s2 = [0,0,0,0,1,1,1,1] # s2 values

# 1D array for raw sensor readings (original format)
signal_reading = [0,0,0,0,0,0,0,0] # Initialise signal_reading
chess_init = [[1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [1,1,1,1,1,1,1,1], [1,1,1,1,1,1,1,1]]

# 2D array for chessboard representation (8x8 board)
# board[row][col] where row 0 = rank 8, row 7 = rank 1
# col 0 = file A, col 7 = file H
chessboard = [[0 for _ in range(8)] for _ in range(8)]

# Chess notation mapping
files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

# Mapping from multiplexer channel to chess square
# You may need to adjust this based on your physical board wiring
# def channel_to_square(channel):
#     """Convert multiplexer channel (0-7) to chess square notation"""
#     if channel < 8:
#         row = channel // 8
#         col = channel % 8
#         return files[col] + ranks[row]
#     return "Invalid"

def square_to_coords(square):
    """Convert chess square notation (e.g., 'A1') to board coordinates"""
    if len(square) != 2:
        return None, None
    file_char = square[0].upper()
    rank_char = square[1]
    
    if file_char in files and rank_char in ranks:
        col = files.index(file_char)
        row = ranks.index(rank_char)
        return row, col
    return None, None

###############################################################################
###############################################################################
###################### --- All helper functions --- ###########################
###############################################################################

def current_readings():
    """Read all multiplexer channels and update both 1D and 2D arrays"""
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    print()
    print("Chessboard readings at " + stamp + " : ")
    print("=" * 50)
    
    # Read all 8 channels
    for i in range(8):
        GPIO.output(S0_PIN, s0[i]) # s0_pin
        GPIO.output(S1_PIN, s1[i]) # s1_pin
        GPIO.output(S2_PIN, s2[i]) # s2_pin
        time.sleep(0.001)  # Small delay for signal stability
        
        signal = GPIO.input(SIG_PIN)
        signal_reading[i] = 1 if signal else 0
        
        # Update 2D chessboard array
        # Note: This assumes first 8 channels map to first col
        # You'll need to adjust mapping based on your physical setup

        # Made a change so its reading first column - Steph
        if i < 8:
            row = i
            col = 0
            chessboard[row][col] = signal_reading[i]
        
        # Display with chess notation
        square = files[col] + ranks[row]
        print(f"Channel {i:2d} [{square}] = "f"{s0[i]}{s1[i]}{s2[i]}  Reading: {signal_reading[i]}")
    
    print("-" * 50)

def display_chessboard():
    """Display the chessboard in a visual 8x8 grid"""
    print("\nChessboard State:")
    print("  " + " ".join(files))
    print("  " + "-" * 15)
    
    for row in range(8):
        row_display = ranks[row] + "|"
        for col in range(8):
            piece = "●" if chessboard[row][col] else "○"
            row_display += piece + " "
        print(row_display)
    print()

def get_square_state(square):
    """Get the state of a specific chess square"""
    row, col = square_to_coords(square)
    if row is not None and col is not None:
        return chessboard[row][col]
    return None

def set_square_state(square, state):
    """Set the state of a specific chess square"""
    row, col = square_to_coords(square)
    if row is not None and col is not None:
        chessboard[row][col] = state
        return True
    return False

def find_changes(current_board, previous_board):
    """Find changes between current board and previous board state"""
    changes = []
    for row in range(8):
        for col in range(8):
            if current_board[row][col] != previous_board[row][col]:
                square = files[col] + ranks[row]
                old_state = previous_board[row][col]
                new_state = current_board[row][col]
                changes.append({
                    'square': square,
                    'from': old_state,
                    'to': new_state,
                    'action': 'placed' if new_state == 1 else 'removed'
                })
    return changes

def copy_board():
    """Create a deep copy of the current board state"""
    return [row[:] for row in chessboard]


###############################################################################
###############################################################################
############################ --- The Magic --- ################################
###############################################################################

def main():
    previous_board = copy_board()
    board = chess.Board()
    
    try:
        while True:
            current_readings()
            
            # Check for changes
            changes = find_changes(chessboard, previous_board)
            if changes:
                legal_moves = board.legal_moves
                print(f"\nDetected {len(changes)} change(s):")
                for change in changes:
                    print(f"  {change['square']}: piece {change['action']}")
            
            display_chessboard()
            previous_board = copy_board()
            
            time.sleep(0.5)  # Slightly longer delay for chess moves
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        GPIO.cleanup()

if __name__ == "__main__":
    main()

###############################################################################
################################ --- Notes --- ################################
###############################################################################
#
# TODO: Adjust channel_to_square mapping based on physical board layout
# TODO: Implement full 64-square reading (you'll need 8 multiplexers or 
#       a different approach for a full 8x8 board)
# TODO: Add move detection logic (from-to square analysis)
# TODO: Add game state tracking
# TODO: Add UCI/PGN notation support
#
###############################################################################
