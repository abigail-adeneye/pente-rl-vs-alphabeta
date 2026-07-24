# Design, code, and train a reinforcement learning (RL) player
# to play the game

'''
- agent interacts with environment
- discrete time steps 0,1,2,....
- at each time step
    - agent senses the state S_t
    - selects an action a_t in A(S_t)
    - executes that action and at the next time step t+1, recieves
      a reward r_(t+1) and finds itself in state S_(t+1)


policy- defines the agents way of behaving at a given time
reward signal- defines the goal of a rl problem
value function- total amount of reward an agent can expect to accumulate 
                over the future, starting from that state
model for the environment
    - mimics the bahavior of the environment
    - allows inferences to be made about how the environment will behave

'''

import os
import pickle
import math
import random
from alpha_beta import get_possible_moves, computer_move
from eval_func import Score_Rubric

# parameters
ALPHA         = 0.1 #learning rate
GAMMA         = 0.9 #discount factor
EPSILON_START = 1.0 # start exploration rate at
EPSILON_END   = 0.05 #smallest exploration rate

REWARD_WIN          =  1.0
REWARD_LOSS         = -1.0 #penalty
REWARD_DRAW         =  0.0
REWARD_CAPTURE_PAIR =  0.05
REWARD_OPP_CAPTURE  = -0.03 #penalty when opponent captures a pair


# Count consecutive stones for a player in a given direction.
#cant use function in pente because it doesnt take board as a parameter. Learned from mistake :(
def count_stones(board, row, col, player, d_row, d_col):
    SIZE = 19

    count = 0
    r = row + d_row # move one step in row
    c = col + d_col # move one step in column

    while (0 <= r < SIZE and 0 <= c < SIZE and board[r][c] == player):
        count += 1 # found same player's stone
        r += d_row # step further
        c += d_col

    return count # return total consecutive stones

# Check all four directions for 5-in-a-row. Return True if any direction has 5 or more stones
#cant use function in pente because it doesnt take board as a parameter. Learned from mistake :(
def check_five_in_row(board, row, col, player):
    for d_row, d_col in [(1,0),(0,1),(1,1),(1,-1)]: #vertical, horizontal, diagonal\, diagonal/
        count = 1 # include the stone just placed
        count += count_stones(board, row, col, player,  d_row,  d_col) # forward
        count += count_stones(board, row, col, player, -d_row, -d_col) #backward
        if count >= 5:
            return True
    return False


'''
Alpha-Beta can return none when Score_Rubric hits >= 1,000,000
at the root of the search tree. Happens cus the eval function can reach 1,000,000 by summing multiple open 4 patterns,
not just an acttual 5 in a row win
When that happens, maxValue() treats it as a terminal state and returns (payoff, None) with no move.
So handle it here by scoring every legal move and picking the best one manually.
'''
def safe_computer_move(board, black_caps, white_caps):
    # Try to get a move from the Alpha-Beta agent normally
    move = computer_move(board, black_caps, white_caps)
    
    # If Alpha-Beta returned a valid move, just use it
    if move is not None:
        return move

    #get move
    import copy
    from Pente import check_captures as pente_check_captures

    best_score = -float('inf') # track the highest score seen so far
    best_move  = None # track which move produced that score
    
    # Loop through every legal move available on the board
    for r, c in get_possible_moves(board):
        # deep copy to not modify the real board
        temp = copy.deepcopy(board)
        temp[r][c] = 'B'
        caps  = pente_check_captures(temp, r, c, 'B') #check capture for move
        #score the board
        score = Score_Rubric(temp, 'B', black_caps + caps, white_caps)
        # If this move scored better than anything seen so far, save it
        if score > best_score:
            best_score = score
            best_move  = (r, c)
    return best_move



# This takes the 19x19 list and turns it into one string of 361 characters
def get_state_string(board, black_caps, white_caps):
    flat = "".join("".join(row) for row in board)
    return f"{flat}{black_caps}{white_caps}"


# Softmax- Action selection
'''soft max for choosing an action
with prob p(a) = (e^(Q_t(a))) / (SUM a of e^(Q_t(a)))
(Q^t)(a) = true expected value of action a
Q_t(a) = estimate of (Q^t)(a) given what we've experienced unto time t
'''
def soft_max(actions, q_values):
    #Choose action a with prob p(a).

    #subtract max q_value to prevent math.exp overflow
    max_q = max(q_values)

    # get numerator e^(Q_t(a))     
    numerators = [math.exp(q - max_q) for q in q_values]

    #get the denominator 
    #SUM a of e^(Q_t(a))
    denom = sum(numerators)
    #get p(a)
    probs = [n / denom for n in numerators]
    Selected_action =  random.choices(actions, weights=probs, k=1)[0]
    return Selected_action


'''
Generate a random number between 0 and 1
- If it falls below epsilon, explore by picking a random move.
    - Early in training epsilon is close to 1.0, so this will happen almost
        every turn. rl tries random moves to discover new strategies.
    - As training progresses epsilon reduces toward 0.05, so this happens
    less and less often.
- Otherwise, use what the agent has already learned.
     - soft_max() picks a move based on Q-values that gives higher-valued
        moves a higher prob of being selected.
'''
def epsilon_greedy(actions, q_values, epsilon):
    if random.random() < epsilon:
        return random.choice(actions)
    return soft_max(actions, q_values)


'''
Choose the best move for the RL agent during the real game.
Called by Pente.py:  row, col = get_best_move(board, q_table)
'''
def get_best_move(board, q_table, black_caps=0, white_caps=0):
    possible_moves = get_possible_moves(board)
    state = get_state_string(board, black_caps, white_caps)

    # Count how many moves have actually been updated, for debug
    updated = [q_table.get((state, m), 0.0) for m in possible_moves
               if q_table.get((state, m), 0.0) != 0.0]
    #DEBUG
    if updated:
        print(f"RL Brain: I recognize this state! Found {len(updated)} moves with Q-values.")
    else:
        print("  RL Brain: Unseen state — choosing best Q (may default to 0).")

    best_q = -float('inf')
    best_move = random.choice(possible_moves)

    #go through the possible moves, get the q val for all moves then compare
    #  it with the best move. If the best move is less, best move = q val
    for move in possible_moves:
        q_val = q_table.get((state, move), 0.0)
        if q_val > best_q:
            best_q    = q_val
            best_move = move
    return best_move


# Q-update with learning rate
'''
the update rule for the q values after a move
Q_(k+1) = Q_k + (1/(k+1))(r_(k+1) - Q_k)- this means
new value = old value + step size(target - old value)
- use constant for the step size instead 
    - cus 1/(k+1) shrinks to nearly 0 after 10 - 20 visits and causes the 
        agent to stop learning too early 
    - consytant alpha = 0.1 keeps the updates meaningful throughout the entire training process.
'''
def update_q(q_table, k_table, state, action, target):
     #target= reward recieved
    # k = # of times we have played this action before
    # old_val (Q_k)
    old_val = q_table.get((state, action), 0.0)

    new_val = old_val + ALPHA * (target - old_val)

     # Save back to tables
    q_table[(state, action)] = new_val
    k_table[(state, action)] = k_table.get((state, action), 0) + 1
    return new_val



'''
Expected Return
Calculates the total discounted reward
and updates the Q-table for all moves made during the game.

Walk backwards through the RL agent's move history and update each
Q-value using discounted expected return- R_t = r_t + gamma * R_(t+1)
'''
def calculate_expected_return(history, final_reward, q_table, k_table, gamma=GAMMA):
    R = final_reward
    for state, action, step_reward in reversed(history):
        R = step_reward + gamma * R
        update_q(q_table, k_table, state, action, R)


# Training loop for rl
'''
Train the RL agent by playing against Alpha-Beta
RL = White(W),  Alpha-Beta = Black(B)

episodes- number of training games
print_every- how often to print (every n episodes)
'''
def train_RL_player(episodes, gamma=GAMMA, print_every=50):
    
    from Pente import check_captures

    q_table, k_table = load_trained_q_table()

    wins    = 0
    losses  = 0
    draws   = 0
    epsilon = EPSILON_START
    eps_step = (EPSILON_START - EPSILON_END) / max(1, episodes)



    for episode in range(1, episodes + 1):
        board          = [['-' for _ in range(19)] for _ in range(19)]
        black_caps     = 0
        white_caps     = 0
        current_player = 'B'
        history        = [] # Stores (S_t, a_t)
        final_reward   = REWARD_DRAW

        while True:
            possible_moves = get_possible_moves(board)
            #  Check for a tie (Board Full)
            if not possible_moves:
                draws += 1
                final_reward = REWARD_DRAW # No winner
                break

            #  Black: Alpha-Beta 
            if current_player == 'B':
                move = safe_computer_move(board, black_caps, white_caps)

                # Safety check: if Alpha-Beta is stuck or board is full
                if move is None:
                    draws += 1
                    final_reward = REWARD_DRAW #Treat as a tie/draw
                    break

                row, col = move
                board[row][col] = 'B'
                black_caps += check_captures(board, row, col, 'B')

                if check_five_in_row(board, row, col, 'B') or black_caps >= 5:
                    losses += 1
                    final_reward = REWARD_LOSS # RL Agent Lost
                    break

            # White: RL agent
            else:
                #agent senses the state S_t
                s_t = get_state_string(board, black_caps, white_caps)

                # Look up the estimated values Q_t(a) for each possible move
                # If we haven't seen a move before, we initialize it to 0.0
                q_vals = [q_table.get((s_t, m), 0.0) for m in possible_moves]

                #selects an action a_t in A(S_t)
                a_t = epsilon_greedy(possible_moves, q_vals, epsilon)

                #executes that action and at the next time step t+1, recieves
                #a reward r_(t+1) and finds itself in state S_(t+1)
                row, col = a_t
                board[row][col] = 'W'
                prev_wc = white_caps
                white_caps += check_captures(board, row, col, 'W')

                step_reward = (white_caps - prev_wc) * REWARD_CAPTURE_PAIR
                history.append((s_t, a_t, step_reward))

                if check_five_in_row(board, row, col, 'W') or white_caps >= 5:
                    wins += 1
                    final_reward = REWARD_WIN # RL Agent Won
                    break

            current_player = 'W' if current_player == 'B' else 'B'

        # After the game, update knowledge based on Expected Return
        calculate_expected_return(history, final_reward, q_table, k_table, gamma)
        epsilon = max(EPSILON_END, epsilon - eps_step)

        

    #save info
    save_q_table(q_table, k_table)


    return {'wins': wins, 'losses': losses, 'draws': draws,
            'q_size': len(q_table)}


# Save with consistent file_path
def save_q_table(q_table, k_table, filename="pente_q_table.pkl"):
    # Force the save to happen in the SAME folder as the script
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, filename)
    with open(file_path, 'wb') as f:
        pickle.dump({'q_table': q_table, 'k_table': k_table}, f)
    print(f"  Q-table saved: {len(q_table):,} entries → {file_path}")


#  creates a full path to the file in the same folder as the script
#load the file
def load_trained_q_table(filename="pente_q_table.pkl"):
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, filename)
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        q_table = data.get('q_table', {})
        k_table = data.get('k_table', {})
        print(f"  Q-table loaded: {len(q_table):,} entries from {file_path}")
        return q_table, k_table
    except FileNotFoundError:
        print(f"  No Q-table at {file_path} — starting fresh.")
        return {}, {}



if __name__ == "__main__":
    print("=" * 60)
    print("  Pente RL Agent — Training")
    print("=" * 60)
    print("RL = White,  Alpha-Beta = Black \n")
    #Each run adds to existing Q-table 

    # Increase total_episodes for a stronger agent
    total_episodes = 5000
    chunk_size     = 100

    print(f"Planning {total_episodes} episodes in chunks of {chunk_size}.")
    print(f"alpha={ALPHA}, gamma={GAMMA}, eps {EPSILON_START}→{EPSILON_END}\n")

    for x in range(0, total_episodes, chunk_size):
        n = min(chunk_size, total_episodes - x)
        print(f"\n--- Chunk {x//chunk_size+1}: "f"eps {x+1}–{x+n} ---")
        train_RL_player(episodes=n, print_every=10)
        print(f"  Saved. ({x+n}/{total_episodes} done)")

    print("\nAll training complete!")
