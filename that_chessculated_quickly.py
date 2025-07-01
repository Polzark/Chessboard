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
# chess module:
# https://python-chess.readthedocs.io/en/latest/index.html
#
# Inspired by: 
# https://forums.raspberrypi.com/viewtopic.php?t=267959
#
# Chess wiki:
# https://chess.fandom.com/wiki/Notation#Algebraic_notation
#
###############################################################################

###############################################################################
###################### --- Initial Setup Stuff --- ############################
###############################################################################

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.OUT) # s0
GPIO.setup(13, GPIO.OUT) # s1
GPIO.setup(15, GPIO.OUT) # s2
GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)  #Signal Input

s0 = [0,1,0,1,0,1,0,1] # s0 values
s1 = [0,0,1,1,0,0,1,1] # s1 values
s2 = [0,0,0,0,1,1,1,1] # s2 values
signal_reading = [0,0,0,0,0,0,0,0] # Initialise signal_reading

board = chess.Board()

rows, cols = (8, 8)
# Cali's part: Creating a 8x8 array for the chessboard, all initialised to 0.
# Might changed later after Cali finishes her implementation.
chessboard_binary_curr = [[0 for i in range(cols)] for j in range(rows)]

# Last reading cycle's chessboard data.
chessboard_binary_prev = [[0 for i in range(cols)] for j in range(rows)]

# Rows are reversed to start from bottom left: A1
chessboard_square = [[chess.square(file, 7 - rank)
                      for file in range(cols)] for rank in range(rows)]

# Might use this to light up particular squares on the chessboard.
# 0 for unlit squares, 1 for lit squares.
chessboard_light_up = [[0 for i in range(cols)] for j in range(rows)]

###############################################################################

###############################################################################
###################### --- All helper functions --- ###########################
###############################################################################

def current_readings():
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

    print()
    print("Multiplexer readings at " + stamp + " : ")
    print("----------------------")

    for i in range(8):
        GPIO.output(11,s0[i]) # s0_pin
        GPIO.output(13,s1[i]) # s1_pin
        GPIO.output(15,s2[i]) # s2_pin

        signal = GPIO.input(18)
        if signal:
            signal_reading[i] = 1
        else:
            signal_reading[i] = 0

        print(i," = ", s0[i],s1[i],s2[i],"Reading: ",signal_reading[i])

    print("-----------------------")

# Can be integrated into the current_readings loop but separated for now.
# Currently, accounts for only the first column of the chessboard lol.
def put_sig_reading_in_chessboard():
    for row in range(8):
        chessboard_binary_curr[row][0] = signal_reading[row]

# Col = file (eg. A), Row = rank (eg. 1)
# returns an array of squares.
# Can get file and rank by using:
#   chess.square_file(square: chess.Square)→ int
#   chess.square_rank(square: chess.Square)→ int
def get_legal_moves(file, rank):
    # Do stuff
    curr_square = chess.square(file, rank)
    curr_piece = board.piece_at(curr_square)

    if curr_piece is None:
        print("EEK! get_legal_moves died lol")
        return

    legal_moves = []
    for curr_legal_move in board.legal_moves:
        if curr_legal_move.from_square == curr_square:
            legal_moves.append(curr_legal_move.to_square)
    
    return legal_moves
        
def light_up_squares(legal_moves):
    # Do more stuff
    pass

def move_piece(from_square, to_square):
    # Do even more stuff lol
    # Might use:
    # remove_piece_at(square: chess.Square)→ Piece | None
    # set_piece_at(square: chess.Square, piece: Piece | None, promoted: bool = False)→ None
    pass

###############################################################################

###############################################################################
############################ --- The Magic --- ################################
###############################################################################

def main():
    try:
        while True:
            current_readings()
            put_sig_reading_in_chessboard()
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__=="__main__":
	main()
    
###############################################################################
