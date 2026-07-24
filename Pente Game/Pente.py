'''
HOW TO PLAY THE PENTE GAME
---------------------------
Setup: Players take turns placing one stone of their color on any empty
intersection of the 19x19 board.

The Goal: The first player to get five stones in a row (horizontally,
vertically, or diagonally) or to capture 5 pairs (10 stones total) of the
opponent's stones wins.

Capturing: You capture pairs of opponent stones by flanking them on both
sides with your own stones (e.g., your stone - enemy stone - enemy stone - your stone).
You can only capture with exactly 2 enemy stones (in between your stones) at a time

Movement: Once a stone is placed, it never moves unless it is captured
and removed from the board

Functions
----------
- print the board(show the board with 19 rows and 19 columns)
- Check if the players plays a valid move
- Count the consecutive stones for a player in a given direction
- Check a specific direction for 5 in a row (diagonal, vertical,
horizontal)
- Check all 4 directiions for 5 in a row (|, -, /, 1)
- Check if the given coordinate is actually on the board
- Check all 8 directions for captures mae by the last move
- Play game - calls all the functions - main game loop to play pente
'''
from alpha_beta import computer_move
from rl_player import load_trained_q_table, get_best_move
#board size is 19*19
SIZE = 19

# We can create the board as a 2D array, all cells initialized as empty '-'
board = [['-' for _ in range(SIZE)] for _ in range(SIZE)]

# Variables to track capture counts for each player
black_captures = 0
white_captures = 0


# Display the board with row and column numbers at the side and top
def print_board():
    # Print column numbers f
    print(" ", " ", end="")
    for i in range(SIZE):
        print(f"{i+1:2}", end=" ")
    print() # new line after column headers

    # Print each row of the board with its row number
    for i in range(SIZE):
        print(f"{i+1:2} ", end="")
        for j in range(SIZE):
            print(f" {board[i][j]} ", end="")
        print() # new line after each row


# Check if a player's move is valid. Returns true if the move is inside the board else return false
def is_move_valid(row, col):
    if 0 <= row < SIZE and 0 <= col < SIZE:
        if board[row][col] == '-':
            return True #cell is empty
        else:
            return False #cell is occupied
    else :
        return False # move is not valid
    

# Count consecutive stones for a player in a given direction.
def count_stones(row, col, player, d_row, d_col):
    count = 0
    r = row + d_row # move one step in row
    c = col + d_col # move one step in column

    while (0 <= r < SIZE and 0 <= c < SIZE and board[r][c] == player):
        count += 1 # found same player's stone
        r += d_row # step further
        c += d_col

    return count # return total consecutive stones


# Check a specific direction (row(vertical), column(horitzontal), diagonal) for 5-in-a-row. Returns True if 5 or more stones in line, else False
def check_direction(row, col, player, d_row, d_col):
    count = 1 # include the stone just placed
    count += count_stones(row, col, player, d_row, d_col) # forward
    count += count_stones(row, col, player, -d_row, -d_col) # backward
    return count >= 5


# Check all four directions for 5-in-a-row. Return True if any direction has 5 or more stones
def check_five_in_row(row, col, player):
    return (
        check_direction(row, col, player, 1, 0) or # vertical
        check_direction(row, col, player, 0, 1) or # horizontal
        check_direction(row, col, player, 1, 1) or # diagonal \
        check_direction(row, col, player, 1, -1) # diagonal /
    )


# Check if coordinates are inside the board limits.
def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


# Check all 8 directions for captures made by the last move.
# Output: Number of pairs captured this move
# Looks for pattern: player - opponent - opponent - player and remove captured opponent stones and increments count
def check_captures(board, row, col, player):
    captures = 0
    opponent = 'W' if player == 'B' else 'B'

    directions = [
        (1,0), (0,1), (1,1), (1,-1),
        (-1,0), (0,-1), (-1,-1), (-1,1)
    ]

    for d_row, d_col in directions:
        r1, c1 = row + d_row, col + d_col
        r2, c2 = row + 2*d_row, col + 2*d_col
        r3, c3 = row + 3*d_row, col + 3*d_col
    
        # Check pattern for capture
        if (in_bounds(r3, c3) and board[r1][c1] == opponent and board[r2][c2] == opponent and board[r3][c3] == player):
            board[r1][c1] = '-'
            board[r2][c2] = '-'
            captures += 1

    return captures



# Main game loop to play Pente. Game runs until a player wins
# Logic:
# 1. Show board
# 2. Ask current player for move
# 3. Validate move
# 4. Place stone
# 5. Check captures
# 6. Update capture counts
# 7. Check win conditions
# 8. Switch players

def play_game():
    global black_captures, white_captures

    # Reset everything for a fresh game when running tournament
    #board = [['-' for _ in range(SIZE)] for _ in range(SIZE)]
    black_captures = 0
    white_captures = 0

    current_player = 'B' # Black starts first

    
    # Load the learned Q-table from  training
    
    q_table, k_table = load_trained_q_table()
        

    while True:
        print_board()
        print(f"Black captures: {black_captures} | White captures:{white_captures}")
        print(f"Player {current_player}'s turn")


        #Computer's turn
        if current_player == 'B':
            '''
            #print("Computer is thinking")
            print('Alpha Beta Agent (Black) is thinking... ')
            from rl_player import safe_computer_move
            move = safe_computer_move(board, black_captures, white_captures)
            if move is None:
                print("No valid move found. Draw.")
                return 'draw'
            row, col = move
            print(f"Alpha Beta plays at {row + 1}, {col + 1} ")
            '''

            #Human's turn
            # Get player input

            row = int(input("Enter row (1-19): "))
            col = int(input("Enter col (1-19): "))
            row = row - 1
            col = col - 1

        else: 
            
            #Human's turn
            # Get player input
            '''
            row = int(input("Enter row (1-19): "))
            col = int(input("Enter col (1-19): "))
            row = row - 1
            col = col - 1
            '''
            
            #Rl turn
            print("RL Agent (White) is thinking...")
            row, col = get_best_move(board, q_table)
            print(f"RL plays at {row + 1}, {col + 1}")
            

        # Validete move
        if not is_move_valid(row, col):
            print("Invalid move. Try again.")
            continue

        # Place stone
        board[row][col] = current_player

        # Check captures
        captures = check_captures(board, row, col, current_player)

        # Update capture counts
        if current_player == 'B':
            black_captures += captures
        else:
            white_captures += captures

        # Check if player won
        if (
            check_five_in_row(row, col, current_player) or
            black_captures >= 5 or
            white_captures >= 5
        ):
            print_board()
            print(f"Player {current_player} wins!")
            return current_player
            
        
        #Switch player for next turn
        current_player = 'W' if current_player == 'B' else 'B'


# Run the game
if __name__ == "__main__":
    play_game()









