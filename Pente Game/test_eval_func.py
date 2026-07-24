# test_eval.py
from eval_func import Score_Rubric

# Create a mock board (all empty)
test_board = [['-' for _ in range(19)] for _ in range(19)]

# Test Case 1: Empty board should be near 0
print(f"Empty Score: {Score_Rubric(test_board, 'B', 0, 0)}")

# Test Case 2: Vertical 3-in-a-row for Black
test_board[5][5] = 'B'
test_board[6][5] = 'B'
test_board[7][5] = 'B'
# This should return around +1000 based on your rubric
print(f"Black Tria Score: {Score_Rubric(test_board, 'B', 0, 0)}")

# Test Case 3: A threat for the opponent
test_board[10][10] = 'W'
test_board[10][11] = 'W'
test_board[10][12] = 'W'
test_board[10][13] = 'W'
# This should drastically lower the score because White has a 'Tessera'
print(f"White Threat Score: {Score_Rubric(test_board, 'B', 0, 0)}")