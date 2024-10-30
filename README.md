A variation of Tic-Tac-Toe in which each player has 3 small pieces, 3 medium pieces, and 2 large pieces.
Players can only place bigger pieces over opponents' pieces.
Win by getting 3 in a row or having more pieces on the board if there are no more moves.

AI Logic
AI uses minimax to go through all game states.
Similar game states (rotated or flipped) are transposed to minimize redundant calculations.
Each game state is stored in a .pkl file to determine the best move.
All the states found are stored to minimize look-up time at the cost of space.

Alpha-beta pruning could be added to minimize live look-up time, however since all states are calculated and stored, this wasn't needed.
