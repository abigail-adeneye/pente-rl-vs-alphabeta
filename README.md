# Pente: Reinforcement Learning vs. Alpha-Beta Pruning

A from-scratch implementation of the board game Pente (19x19 grid, win by 5-in-a-row or 5 captured pairs), built to compare two different AI approaches head-to-head: a hand-crafted alpha-beta search agent and a self-trained reinforcement learning agent.

## Overview

- **Black (Alpha-Beta agent):** searches the game tree using minimax with alpha-beta pruning, scoring each board state with a hand-designed evaluation function.
- **White (RL agent):** learns entirely from self-play using tabular Q-learning — no hand-coded strategy, just a Q-table built up over training episodes.

The two agents are trained/tested against each other, and results are tracked in a tournament script.

## How it works

### Alpha-Beta Agent (`alpha_beta.py`, `eval_func.py`)
- Minimax search with alpha-beta pruning, searching to a fixed depth.
- Candidate moves are limited to empty cells within a 2-square radius of existing stones, which keeps the branching factor manageable on a 19x19 board.
- Board states are scored by `Score_Rubric()`, which combines:
  - **Line scoring** — sliding a 5-cell window across every row, column, and diagonal, scoring partial alignments (2/3/4/5 in a row)
  - **Capture scoring** — non-linear rewards for captured pairs, scaling sharply near the 5-pair win condition
  - **Center control** — a small bonus for stones placed near the board's center

### RL Agent (`rl_player.py`)
- **Tabular Q-learning**, trained via self-play against the alpha-beta agent over thousands of episodes.
- **State representation:** the full 19x19 board flattened into a string, plus each side's capture count.
- **Action selection:** epsilon-greedy — starts fully random (ε = 1.0) and anneals to mostly-greedy (ε = 0.05) over training, with softmax sampling over Q-values when exploiting.
- **Rewards:** +1 for a win, -1 for a loss, 0 for a draw, plus a small shaping bonus (+0.05) for each capture made along the way.
- **Updates:** Q-values are updated backward through each game's move history using discounted expected return (γ = 0.9), with a constant learning rate (α = 0.1) rather than a decaying one, so the agent keeps learning throughout training instead of stalling out after a state's first few visits.
- The trained Q-table is pickled to disk after each training run and reloaded on the next, so training can continue across multiple sessions.

### Game engine (`Pente.py`)
Handles board state, move validation, win detection (5-in-a-row in any of 4 directions), and the flanking-capture rule (bracketing exactly 2 opponent stones removes them from the board).

## Files

| File | Purpose |
|---|---|
| `Pente.py` | Core game engine and main game loop |
| `alpha_beta.py` | Alpha-beta search agent |
| `eval_func.py` | Hand-crafted board evaluation function used by the alpha-beta agent |
| `rl_player.py` | Q-learning agent: training loop, move selection, Q-table persistence |
| `tournament.py` | Runs repeated games between the two agents and reports a win/loss/draw tally |
| `test_eval_func.py` | Sanity checks for the evaluation function against known board patterns |
| `pente_q_table.pkl` | Saved Q-table from a training run |

## Running it

```bash
# Train the RL agent (adjust total_episodes in rl_player.py as needed)
python rl_player.py

# Run a tournament between the trained RL agent and the alpha-beta agent
python tournament.py
```

## Results & analysis

In a 10-game tournament, the alpha-beta agent won every game. This tracks with the size of the problem: Pente's board has roughly 3³⁶¹ possible states, and after training the Q-table held around 24,000 entries — a vanishingly small fraction of the state space. The alpha-beta agent, by contrast, plays at full strength immediately since its evaluation function generalizes to any board state without needing to have seen it before.

**Planned improvements:**
- Significantly more training episodes to expose the Q-learning agent to a wider variety of board states
- A curriculum approach — training against a random opponent first, then introducing the alpha-beta agent once the agent has a baseline policy, rather than training against a strong opponent from move one
