#RL vs Alpha beta
#who will win? 



# Plays the game x times and tracks who wins each game.

from Pente import play_game

#number of games played
num_game = 10

ab_wins  = 0 #alpha beta
rl_wins  = 0
draws    = 0

print(f'Running {num_game} games...\n')

for i in range(1, num_game + 1):
    print(f'--- Game {i} ---')
    result = play_game()   # returns 'B', 'W', or 'draw'

    if result == 'B':
        ab_wins += 1
        print(f'Game {i}: Alpha-Beta (Black) wins\n')
    elif result == 'W':
        rl_wins += 1
        print(f'Game {i}: RL Agent (White) wins\n')
    else:
        draws += 1
        print(f'Game {i}: Draw\n')

print(f'  Games played    : {num_game}')
print(f'  Alpha-Beta wins : {ab_wins} ({ab_wins/num_game*100:.0f}%)')
print(f'  RL Agent wins   : {rl_wins} ({rl_wins/num_game*100:.0f}%)')
print(f'  Draws           : {draws} ({draws/num_game*100:.0f}%)')
