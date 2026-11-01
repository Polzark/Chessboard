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

# Comments are for GPIO.BOARD
LOAD_PIN = 17    # SH/LD
CLOCK_PIN = 27   # CLK
DATA_PIN = 24    # QH
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LOAD_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(CLOCK_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DATA_PIN, GPIO.IN)

# Sensor configuration
PIECE_DETECTED_STATE = GPIO.LOW

# 1D array for raw sensor readings (original format)
signal_reading = [0] * 8
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


def read_shift_register():
    """Read all 8 inputs from the SN74HC165."""

    # Assuming input is:
    # A B C D
    # H G F E

    bits = []

    # Load all parallel inputs
    GPIO.output(LOAD_PIN, GPIO.LOW)
    time.sleep(0.00001)
    GPIO.output(LOAD_PIN, GPIO.HIGH)

    for i in range(8):
        bits.append(GPIO.input(DATA_PIN))

        # Shift to the next bit
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)

    return bits


# def square_to_coords(square):
#     """Convert chess square notation (e.g., 'A1') to board coordinates"""
#     if len(square) != 2:
#         return None, None
#     file_char = square[0].upper()
#     rank_char = square[1]
    
#     if file_char in files and rank_char in ranks:
#         col = files.index(file_char)
#         row = ranks.index(rank_char)
#         return row, col
#     return None, None

###############################################################################
###############################################################################
###################### --- All helper functions --- ###########################
###############################################################################

def current_readings():
    """Read all multiplexer channels and update both 1D and 2D arrays"""
    global signal_reading, chessboard

    signal_reading = read_shift_register()

    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    print()
    print("Chessboard readings at " + stamp + " : ")
    print("=" * 50)

    chessboard = [
        [1 if reading == PIECE_DETECTED_STATE else 0 for reading in signal_reading[0:4]],
        [1 if reading == PIECE_DETECTED_STATE else 0 for reading in signal_reading[4:8]]
    ]
            
    # Read all 8 channels
    for i in range(8):
        position = i + 1
        reading = signal_reading[i]

        status = "HIGH" if reading else "LOW"
        
        print(f"Position {position}: {status} ({reading})")
    
    print("-" * 50)

def display_chessboard():
    """Display the chessboard in a visual 8x8 grid"""
    print("\nChessboard State:")
    print("  " + " ".join(files))
    print("  " + "-" * 15)
    
    for row in range(2):
        row_display = ranks[row] + "|"
        for col in range(4):
            piece = "●" if chessboard[row][col] else "○"
            row_display += piece + " "
        print(row_display)
    print()

# def get_square_state(square):
#     """Get the state of a specific chess square"""
#     row, col = square_to_coords(square)
#     if row is not None and col is not None:
#         return chessboard[row][col]
#     return None

# def set_square_state(square, state):
#     """Set the state of a specific chess square"""
#     row, col = square_to_coords(square)
#     if row is not None and col is not None:
#         chessboard[row][col] = state
#         return True
#     return False

def find_changes(current_board, previous_board):
    """Find changes between current board and previous board state"""
    changes = []
    for row in range(2):
        for col in range(4):
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

def wait_for_start():
    print("Waiting for a magnet at position H...")

    while True:
        readings = read_shift_register()

        if readings[0] == PIECE_DETECTED_STATE:
            print("Magnet detected at H. Starting...")
            return

        time.sleep(0.1)

def main():
    wait_for_start()

    current_readings()
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
