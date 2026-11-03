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


LOAD_PIN = 17
CLOCK_PIN = 27
DATA_PIN = 24

PIECE_DETECTED_STATE = GPIO.LOW

if GPIO.getmode() is None:
    GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

GPIO.setup(LOAD_PIN, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(CLOCK_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(DATA_PIN, GPIO.IN)

SENSOR_LAYOUT = [
    [8, 9, 10, 11],
    [12, 13, 14, 15],
    [0, 1, 2, 3],
    [4, 5, 6, 7]
]

ROWS = len(SENSOR_LAYOUT)
COLS = len(SENSOR_LAYOUT[0])
SENSOR_COUNT = ROWS * COLS

files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

# Logical board state: 1 = magnet detected, 0 = empty
chessboard = [[0 for _ in range(COLS)] for _ in range(ROWS)]

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


def read_shift_register():
    """Read all 16 sensor signals from the two daisy-chained HC165s."""
    bits = []

    # Capture parallel sensor states
    GPIO.output(LOAD_PIN, GPIO.LOW)
    time.sleep(0.00001)
    GPIO.output(LOAD_PIN, GPIO.HIGH)

    # Read serial output
    for _ in range(SENSOR_COUNT):
        bits.append(GPIO.input(DATA_PIN))

        GPIO.output(CLOCK_PIN, GPIO.HIGH)
        GPIO.output(CLOCK_PIN, GPIO.LOW)

    return bits


def current_readings():
    readings = read_shift_register()

    for row in range(ROWS):
        for col in range(COLS):
            sensor_index = SENSOR_LAYOUT[row][col]
            occupied = readings[sensor_index] == PIECE_DETECTED_STATE

            chessboard[row][col] = occupied

    return readings

def current_readings_and_print():
    global chessboard

    readings = read_shift_register()

    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    print()
    print("Chessboard readings at " + stamp + " : ")
    print("=" * 50)

    for row in range(ROWS):
        for col in range(COLS):
            sensor_index = SENSOR_LAYOUT[row][col]

            occupied = readings[sensor_index] == PIECE_DETECTED_STATE
            chessboard[row][col] = 1 if occupied else 0

            status = "LOW" if occupied else "HIGH"
            
            print(f"Position ({row}, {col}): {status} ({readings[sensor_index]})")

    print("-" * 50)

    return readings


def display_chessboard():
    """Display the chessboard in a visual 8x8 grid"""
    print("\nChessboard State:")
    print("  " + " ".join(files))
    print("  " + "-" * 15)
    
    for row in range(ROWS):
        row_display = ranks[row] + "|"
        for col in range(COLS):
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
    for row in range(ROWS):
        for col in range(COLS):
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
    print("Waiting for a magnet at position a8...")

    while True:
        readings = read_shift_register()

        if readings[SENSOR_LAYOUT[0][0]] == PIECE_DETECTED_STATE:
            print("Magnet detected at a8. Starting...")
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

    finally:
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
