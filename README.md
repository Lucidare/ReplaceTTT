# Replace-Tic-Tac-Toe

A twist on classic Tic-Tac-Toe, this game adds a new level of strategy with varied piece sizes and unique rules for replacing opponent pieces. 

## Game Overview
- Each player starts with **3 small**, **3 medium**, and **2 large pieces**.
- Players may **place larger pieces over their opponent's smaller pieces** to gain control.
- The objective is to either:
  - **Get 3 in a row** (horizontally, vertically, or diagonally), or
  - **Control more pieces on the board** when no valid moves are left.

## AI Logic
The AI in this game uses **minimax** with stored game states for optimal decision-making:

- **Minimax Algorithm**: Calculates all possible future game states to find the best move, simulating both the AI’s and the player’s optimal moves.
- **Game State Transposition**: To reduce redundant calculations, game states that are similar (rotated or flipped) are transposed and treated as equivalent.
- **Memoization with `.pkl` File**: All unique game states are stored in a `.pkl` file, allowing the AI to retrieve precomputed best moves instantly.
- **Efficiency**: By storing all evaluated states, the AI eliminates live look-up time. Although this approach requires more storage, it significantly reduces response time during gameplay.

> **Note**: **Alpha-beta pruning** could further optimize live look-up, but it is unnecessary here due to the precomputed game states.
