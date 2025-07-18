import chess

board = chess.Board()

print(board)
print()



Nf3 = chess.Move.from_uci("g1f3")
board.push(Nf3)
print(board)
print()



# while not board.is_game_over():
#     print("I'm still aliveee")



rows, cols = (8, 8)
chessboard_square = [[chess.square(file, 7 - rank) 
                      for file in range(cols)] for rank in range(rows)]
print(chessboard_square)



