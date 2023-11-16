import math
import sys
class Node:
    def __init__(self, board):
        self.board = board
        self.children = []
        self.score = None

#Generates positions by removing black pieces.
def generateRemove(board, L):
    for i in range(len(board)):
        if board[i] == 'B':  # Black piece
            if not closeMill(i, board):
                b = list(board)  # Create a copy of the board
                b[i] = 'x'  # Remove black piece
                L.append(b)
    if not L:  # If no positions were added (all black pieces are in mills)
        L.append(list(board))

def getNeighbors(i, board):
  adjacentList = {
      0 : [6],
      1 : [11],
      2 : [3,7],
      3 : [2,10],
      4 : [5,8],
      5 : [4,9],
      6 : [0,7,18],
      7 : [6,8,2,15],
      8 : [7,4,12],
      9 : [5,10,14],
      10 : [3,17,9,11],
      11 : [10,1,20],
      12 : [8,13],
      13 : [16,12,14],
      14 : [13,9],
      15 : [16,7],
      16 : [15,17,19,13],
      17 : [10,16],
      18 : [6,19],
      19 : [16,18,20],
      20 : [19,11]
  }
  neighbors = []
  if i in adjacentList:
    neighbors = adjacentList[i]

  return neighbors

#Check if a move to the given location closes a mill.

def closeMill(location, board):

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

def generateMove(board):
  L = []
  for location in range(len(board)):
    if board[location] == 'W':
      neighbors = getNeighbors(location, board)  # getNeighbors function returns a list of neighboring positions
      for j in neighbors:
        if board[j] == 'x':
          b = list(board)
          b[location] = 'x'
          b[j] = 'W'
          if closeMill(j, b):
            generateRemove(b, L)
          else:
            L.append(b)
  return L

def generateMovesMidgameEndgame(board):
    white_pieces = sum(1 for piece in board if piece == 'W')
    if white_pieces == 3:
        return generateHopping(board)
    else:
        return generateMove(board)


def generateHopping(board):

  L = []

  for location in range(len(board)):
    if board[location] == 'W':
        for j in range(len(board)):
          if board[j] == 'x':
            b = board.copy()
            b[location] = 'x'
            b[j] = 'W'
            if closeMill(j, b):
              generateRemove(b, L)
            else:
              L.append(b)

  return L



#Calculates the static estimation for the given board position.
def static_estimation(board):

    num_white_pieces = board.count('W')
    num_black_pieces = board.count('B')
    L = generateMovesMidgameEndgame(board)
    numBlackMoves = len(L)
    if num_black_pieces <= 2:
        return 10000
    elif num_white_pieces <= 2:
        return -10000
    elif numBlackMoves == 0:
        return 10000
    else:
        return 1000 * (num_white_pieces - num_black_pieces) - numBlackMoves

def build_game_tree(board, depth, alpha, beta, maximizing_player):
    node = Node(board)

    if depth == 0:
        node.score = static_estimation(board)
        return node

    moves = generateMovesMidgameEndgame(board)

    for move in moves:
        temp = board
        board = move 
        child_node = build_game_tree(board, depth - 1, alpha, beta, not maximizing_player)
        board = temp

        node.children.append(child_node)

        if maximizing_player:
            alpha = max(alpha, child_node.score)
            if beta <= alpha:
                break
        else:
            beta = min(beta, child_node.score)
            if beta <= alpha:
                break

    node.score = alpha if maximizing_player else beta

    return node


def find_best_move(board, depth):
    game_tree = build_game_tree(board, depth, float('-inf'), float('inf'), True)

    best_score = float('-inf')
    best_move = None

    for child in game_tree.children:
        if child.score > best_score:
            best_score = child.score
            best_move = child.board

    return best_move


input_file = sys.argv[1]
output_file = sys.argv[2]
depth = int(sys.argv[3])

f = open(input_file, "r")
board = f.read()
#print("initial board: ", board)
p = open(output_file, "w")

moves = generateMovesMidgameEndgame(board)
num_positions_evaluated = len(moves)

best_move = find_best_move(board, depth)

final_board = ''.join(best_move)  # Join the list elements without any separator
p.write(final_board)
print("Board Position:", final_board)
print("Positions evaluated by static estimation:", num_positions_evaluated)
minimax_estimate = static_estimation(final_board)
print("MINIMAX estimate:", minimax_estimate)

