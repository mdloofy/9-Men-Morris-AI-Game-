
import math
import sys

def generateRemove(board, L):   #Generates positions by removing black pieces.
    for i in range(len(board)):
        if board[i] == 'B':  # Black piece
            if not closeMill(i, board):
                b = list(board)  # Create a copy of the board
                b[i] = 'x'  # Remove black piece
                L.append(b)
    if not L:  # If no positions were added (all black pieces are in mills)
        L.append(list(board))



def closeMill(location, board):   #Check if a move to the given location closes a mill.

    piece = board[location]
    if location == 0:
        return (board[6] == piece and board[18] == piece)
    elif location == 6:
        return (board[0] == piece and board[18] == piece) or (board[7] == piece and board[8] == piece)
    elif location == 18:
        return (board[0] == piece and board[6] == piece ) or (board[19] == piece and board[20] == piece)
    elif location == 19:
        return (board[18] == piece and board[20] == piece ) or (board[13] == piece and board[16] == piece)
    elif location == 20:
        return (board[18] == piece and board[19] == piece ) or (board[1] == piece and board[11] == piece)
    elif location == 11:
        return (board[1] == piece and board[20] == piece ) or (board[9] == piece and board[10] == piece)
    elif location == 1:
        return (board[11] == piece and board[20] == piece )
    elif location == 2:
        return (board[7] == piece and board[15] == piece )
    elif location == 7:
        return (board[15] == piece and board[2] == piece ) or (board[6] == piece and board[8] == piece)
    elif location == 15:
        return (board[2] == piece and board[7] == piece ) or (board[16] == piece and board[17] == piece)
    elif location == 16:
        return (board[15] == piece and board[17] == piece ) or (board[19] == piece and board[13] == piece)
    elif location == 17:
        return (board[15] == piece and board[16] == piece ) or (board[3] == piece and board[10] == piece)
    elif location == 10:
        return (board[3] == piece and board[17] == piece ) or (board[9] == piece and board[11] == piece)
    elif location == 3:
        return (board[10] == piece and board[17] == piece )
    elif location == 4:
        return (board[8] == piece and board[12] == piece )
    elif location == 8:
        return (board[4] == piece and board[12] == piece ) or (board[6] == piece and board[7] == piece)
    elif location == 12:
        return (board[4] == piece and board[8] == piece ) or (board[13] == piece and board[14] == piece)
    elif location == 13:
        return (board[12] == piece and board[14] == piece ) or (board[16] == piece and board[19] == piece)
    elif location == 14:
        return (board[12] == piece and board[13] == piece ) or (board[9] == piece and board[5] == piece)
    elif location == 9:
        return (board[14] == piece and board[5] == piece ) or (board[10] == piece and board[11] == piece)
    elif location == 5:
        return (board[9] == piece and board[14] == piece )

    return False

def generateAdd(board):
  L = []
  for i in range(len(board)):
    if board[i] == 'x':
      b = list(board)
      b[i] = 'W'
      if closeMill(i,b):
        generateRemove(b, L)
      else:
        L.append(b)

  return L

def generateMoveOpening(board):   # generate all possible moves 
    L = generateAdd(board)
    return L

def static_estimation(board):    #Calculates the static estimation for the given board position.
    num_white_pieces = board.count('W')
    num_black_pieces = board.count('B')
    return num_white_pieces - num_black_pieces


def minimax(board, depth, maximizing_player):  # Define the MINIMAX search function
    
    if depth == 0:
        return static_estimation(board)

    if maximizing_player:
        max_eval = -math.inf
        for move in generateMoveOpening(board):
            new_board = move    #generateMove(board, move)
            eval = minimax(new_board, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = math.inf
        for move in generateMoveOpening(board):
            new_board = move    #generateMove(board, move)
            eval = minimax(new_board, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def find_best_move(board, depth):   # Function to determine the best move for White
    best_eval = -math.inf
    best_move = None
    for move in generateMoveOpening(board):
        new_board = move    #generateMove(board, move)
        eval = minimax(new_board, depth - 1, False)
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


input_file = sys.argv[1]
output_file = sys.argv[2]
depth = int(sys.argv[3])

f = open(input_file, "r")
board = f.read()
#print("initial board: ", board)
p = open(output_file, "w")

moves = generateMoveOpening(board)
num_positions_evaluated = len(moves)

bestMove = find_best_move(board, depth)
result = ''.join(bestMove)  # Join the list elements without any separator

p.write(result)
print("Board Position:", ''.join(result))
print("Positions evaluated by static estimation:", num_positions_evaluated)
minimax_estimate = static_estimation(result)
print("MINIMAX estimate:", minimax_estimate)