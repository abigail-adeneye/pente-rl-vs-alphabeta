#implement an alpha-beta pruning player

from eval_func import Score_Rubric
import copy

def computer_move(board, black_captures, white_captures):
    score, move = maxValue(board, -float('inf'), float('inf'), 2, black_captures, white_captures)
    return move

'''
Assume we have a function minValue() that computes the value of the subgame 
when min goes first. We want to create maxValue(board).
alpha = value max can guarantee off the current path
beta = value min can guarantee off the current path
'''
def maxValue(board, alpha, beta, depth, black_captures, white_captures):
    from Pente import check_captures
    payoff = Score_Rubric(board, 'B', black_captures,white_captures)
    #if game is over or we reach depth limit, return payoff(Score_Rubric)
    if payoff >= 1000000: #black won
        return payoff, None
    if payoff <= -1000000: #white won
        return payoff, None
    if depth == 0: #reached depth limit
        return payoff, None
    
    #else 
    #set best move so far to null
    best_move = None
    v = -float('inf') #value of best move so far
    #for every possible move, 
    for move in get_possible_moves(board):
        #creating a copy of board to fix the undo when 2 stones are captured
        #so when it undos, we get the stones that were captured
        temp_board = copy.deepcopy(board)
        r, c = move
        #make the move on the board
        temp_board[r][c] = 'B'

        #check for capture on the temp board
        cap = check_captures(temp_board, r, c, 'B')
        temp_black_captures = black_captures + cap

        #v = minValue(board)
        new_v, _ = minValue(temp_board, alpha, beta, depth-1, temp_black_captures, white_captures)
        #undo the move
        #board[r][c] = '-' # not needed anymore since we have a copy

        #if new_v is better, save it
        if new_v > v:
            v = new_v
            best_move = move

        #if v > alpha: alpha = v
        if v > alpha:
            alpha = v
        #prune- if alpha >= beta, return beta
        if alpha >= beta:
            return beta, best_move
    return alpha, best_move

'''
Assume we have maxValue() that computes the value of games when it's max's turn 
'''
def minValue(board, alpha, beta, depth, black_captures, white_captures):
    from Pente import check_captures

    payoff = Score_Rubric(board, 'B', black_captures,white_captures)
    #if game is over or we reach depth limit, return payoff(Score_Rubric)
    if payoff >= 1000000: #black won
        return payoff, None
    if payoff <= -1000000: #white won
        return payoff, None
    if depth == 0: #reached depth limit
        return payoff, None
    
    #else 
    best_move = None
    v = float('inf') #value of best move so far
    #for every possible move, 
    for move in get_possible_moves(board):
        temp_board = copy.deepcopy(board)

        r, c = move
        #make the move on the board
        temp_board[r][c] = 'W'

        #check for capture on the temp board
        cap = check_captures(temp_board, r, c, 'W')
        temp_white_captures = white_captures + cap

        #v = minValue(board)
        new_v, _ = maxValue(temp_board, alpha, beta, depth-1, black_captures, temp_white_captures)
        #undo the move
        #board[r][c] = '-'

        if new_v < v:
            v = new_v
            best_move = move

        #if v < beta: beta = v
        if v < beta:
            beta = v
        #prune- if alpha <= beta, return alpha
        if alpha >= beta:
            return alpha, best_move
    return beta, best_move


#get every possible moves
def get_possible_moves(board):
    moves = set() # Use a set to avoid duplicates
    for r in range(19):
        for c in range(19):
            if board[r][c] != '-':
                # Look in a 2-square radius around every stone
                for dr in range(-2, 3):
                    for dc in range(-2, 3):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 19 and 0 <= nc < 19 and board[nr][nc] == '-':
                            moves.add((nr, nc))
    
    # If the board is totally empty, just return the center square
    if not moves:
        return [(9, 9)]
        
    # sort the moves so they are always in the exact same order for the RL brain
    return sorted(list(moves), key=lambda x: (x[0], x[1]))