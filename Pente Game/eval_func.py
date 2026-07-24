
'''
DESIGN AN EVALUATION FUNCTION
- Create a scoring engine that analyzes the board and returns a single numerical value
  representing who is winning.

Scoring Rubric : Assign points to specific patterns
- Victory (5-in-a-row or 5 captures): +1,000,000 (Game Over).
- Open 4-in-a-row (Tessera): +20,000 (Guaranteed win next turn).
- Capture Pair: +500 per pair captured.
- Open 3-in-a-row (Tria): +1,000 (Must be blocked immediately).
- Center Control: +10 for stones placed near the middle of the board


- 5 stones: +1,000,000
- 4 stones + 1 empty: +21,000
- 3 stones + 2 empty: +1000
- 2 stones + 3 empty: +50

- 1 capture: +500
- 2 captures: +1,000
- 3 captufres: +1,500
- 4 captures: +20,000
- 5 captures: +1,000,000
- Mixed: 0

'''
SIZE = 19

#Scoring Rubric
#get total score
def Score_Rubric(board,player,black_captures, white_captures):
    score = 0
    if player == 'B':
        opponent = 'W' 
    else: 
        opponent = 'B'
    
    #scoring based on stones in a row

    #horizontal
    for i in range(SIZE):
        for j in range (SIZE-4):
            #gets cells from index j to j+5
            cells = [board[i][j+k] for k in range(5)]
            score += Board_Score(cells, player)
    
    #vertical
    for i in range(SIZE):
        for j in range (SIZE-4):
            cells = [board[j+k][i] for k in range(5)]
            score += Board_Score(cells, player)

    #diagonal (\)
    for i in range(SIZE-4):
        for j in range (SIZE -4): 
            cells = [board[i+k][j+k] for k in range(5)]
            score += Board_Score(cells, player)


    #diagonal (/)
    for i in range(SIZE-4):
        for j in range (4, SIZE):
            cells = [board[i+k][j-k] for k in range(5)]
            score += Board_Score(cells, player)

   #add capture scores
    score += Capture_Score(player, black_captures, white_captures)

    # Center Control: for stones in the middle (indices 7 to 11)
    for r in range(7, 12):
        for c in range(7, 12):
            if board[r][c] == player:
                score += 10
            elif board[r][c] != '-': # Opponent stone
                score -= 10


    return score


#get scoring for x in a row
#takes a list of 5 cells and returns a score
def Board_Score(cells, player):
    score = 0
    if player == 'B':
        opponent = 'W' 
    else: 
        opponent = 'B'

    #count how many stones of each type are in the 5 cell window
    player_count = cells.count(player)
    empty_count = cells.count('-')
    opponent_count = cells.count(opponent)


    '''
    - 5 stones: +1,000,000
    - 4 stones + 1 empty: +20,000
    - 3 stones + 2 empty: +1000
    - 2 stones + 3 empty: +50
    - Mixed: 0

    '''
    #if there are mixed types in the cell, score is 0
    if player_count > 0 and opponent_count > 0: 
        return score

    # 1. Scoring for the Player (Max)
    if player_count == 5:
        score += 1000000 # Victory
    elif player_count == 4 and empty_count == 1:
        score += 21000   # Tessera (Open 4)
    elif player_count == 3 and empty_count == 2:
        score += 1000    # Tria (Open 3)
    elif player_count == 2 and empty_count == 3:
        score += 50

    # 2. Scoring for the Opponent (Min)
    # subtract points because this is bad for the player
    if opponent_count == 5:
        score -= 1000000 
    elif opponent_count == 4 and empty_count == 1:
        score -= 21000 
    elif opponent_count == 3 and empty_count == 2:
        score -= 1000
    elif opponent_count == 2 and empty_count == 3:
        score -= 50


    return score

#scoring for the captures
def Capture_Score(player, black_captures, white_captures):
    score = 0
    if player == 'B':
        opponent = 'W' 
        player_captures = black_captures
        opponent_captures = white_captures
    else: 
        opponent = 'B'
        player_captures = white_captures
        opponent_captures = black_captures

    '''
    - 1 capture: +500
    - 2 captures: +1,000
    - 3 captufres: +1,500
    - 4 captures: +20,000
    - 5 captures: +1,000,000
    '''
    #add score for player captures
    if player_captures >= 5:
        score += 1000000
    elif player_captures == 4:
        score += 20000
    elif player_captures == 3:
        score += 1500
    elif player_captures == 2:
        score += 1000
    elif player_captures == 1:
        score+= 500
    else:
        score += 0

    #subtract score for opponent captures
    if opponent_captures >= 5:
        score -= 1000000
    elif opponent_captures == 4:
        score -= 20000
    elif opponent_captures == 3:
        score -= 1500
    elif opponent_captures == 2:
        score -= 1000
    elif opponent_captures == 1:
        score -= 500
    else:
        score -= 0

    return score

