import numpy as np
import pickle
import random
from collections import defaultdict
import time


class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.counts = {
            "X": {"s": 3, "m": 3, "l": 2},
            "O": {"s": 3, "m": 3, "l": 2}
        }
        self.current_player = "X"  # Start with player X

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def check_connect_3(self):
        def all_same_and_valid(items):
            return all(item != " " and item[1] == items[0][1] for item in items)

        # Check rows
        for row in self.board:
            if all_same_and_valid(row):
                return row[0][1]

        # Check columns
        for col in range(3):
            if all_same_and_valid([self.board[0][col], self.board[1][col], self.board[2][col]]):
                return self.board[0][col][1]

        # Check diagonals
        if all_same_and_valid([self.board[0][0], self.board[1][1], self.board[2][2]]):
            return self.board[0][0][1]
        if all_same_and_valid([self.board[0][2], self.board[1][1], self.board[2][0]]):
            return self.board[0][2][1]

        return None

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def can_replace(self, old_piece, new_size):
        # Extract the size of the old piece
        old_size = old_piece[0]

        # Define the size hierarchy
        size_order = {'s': 1, 'm': 2, 'l': 3}

        # Check if the new size is larger than the old size and if the new size is available
        return (size_order[new_size] > size_order[old_size] and
                self.counts[self.current_player][new_size] > 0)

    def make_or_replace_move(self, row, col, size):
        current_piece = self.board[row][col]

        if current_piece == " ":
            if self.counts[self.current_player][size] > 0:
                self.board[row][col] = f"{size}{self.current_player}"
                self.counts[self.current_player][size] -= 1
                return True  # Successful placement
        elif current_piece[1] != self.current_player:
            if self.can_replace(current_piece, size):
                # If replacing, do not give back the old piece
                self.board[row][col] = f"{size}{self.current_player}"
                self.counts[self.current_player][size] -= 1  # Decrement the count for the new piece
                return True  # Successful replacement

        return False  # Invalid move

    def get_valid_moves(self):
        valid_moves = []
        for i in range(3):
            for j in range(3):
                current_piece = self.board[i][j]
                
                # If the cell is empty, check for all piece sizes
                if current_piece == " ":
                    for size in self.counts[self.current_player]:
                        if self.counts[self.current_player][size] > 0:
                            valid_moves.append((i, j, size))  # Add (row, col, size) as a valid move
                else:
                    # If there's a piece already, check if it can be replaced
                    if current_piece[1] != self.current_player:
                        for size in self.counts[self.current_player]:
                            if self.can_replace(current_piece, size):
                                valid_moves.append((i, j, size))  # Add (row, col, size) as a valid replacement move

        return valid_moves


    def remaining_counts(self):
        return self.counts

    def check_game_over(self):
        winner = self.check_connect_3()
        if winner:
            return winner
        if self.is_full():
            (x, o) = self.count_pieces_on_board()
            if x > o:
                return "X"
            elif o > x:
                return "O"
            else:
                return "IMPOSSIBLE"
        return None

    def count_pieces_on_board(self):
        piece_count = {
            "X": 0,
            "O": 0
        }
        
        for row in self.board:
            for cell in row:
                if cell != " ":  # If the cell is not empty
                    piece_count[cell[1]] += 1  # Increment the count for the player

        return piece_count

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

def main():
    playerX = QLearningAgent()  # Agent X
    playerO = QLearningAgent()  # Agent O
    
    # Load the trained Q-table for the agents
    try:
        playerX.load_q_table('q_table_X.pkl')
        print("Loaded Q-table for player X.")
    except FileNotFoundError:
        print("No trained Q-table found for player X.")

    try:
        playerO.load_q_table('q_table_O.pkl')
        print("Loaded Q-table for player O.")
    except FileNotFoundError:
        print("No trained Q-table found for player O.")

    game = TicTacToe()
    
    # Prompt the user to choose their character and the agent to play against
    player_choice = input("Choose your character (X or O): ").strip().upper()
    while player_choice not in ['X', 'O']:
        player_choice = input("Invalid choice. Please choose X or O: ").strip().upper()

    # Determine which agent is the opponent
    agent_player = "O" if player_choice == "X" else "X"  # If player is X, agent is O; if player is O, agent is X

    while game.check_game_over() == None:
        game.print_board()
        print(f"Current player: {game.current_player} - Remaining counts: {game.remaining_counts()}")

        if game.current_player == player_choice:  # Human player's turn
            action = input("Enter 'row col size' to place a piece (sizes: s, m, l): ")
            action_parts = action.split()
            if len(action_parts) == 3:
                row, col, size = action_parts
                row, col = int(row), int(col)
                if game.make_or_replace_move(row, col, size):
                    result = game.check_game_over()
                    if result:
                        game.print_board()
                        if isinstance(result, str):
                            print(f"Winner: {result}")
                        else:
                            print("Game is a draw.")
                        break
                    game.switch_player()
                else:
                    print("Invalid move or not enough pieces available.")
            else:
                print("Invalid action.")
        
        else:  # Agent's turn
            valid_actions = game.get_valid_moves()
            if valid_actions:
                action_index = (playerX if agent_player == "X" else playerO).choose_action(game.board, valid_actions)
                (row, col, size) = valid_actions[action_index]  # Get the row, col, size from valid actions
                game.make_or_replace_move(row, col, size)

                result = game.check_game_over()
                if result:
                    game.print_board()
                    if isinstance(result, str):
                        print(f"Winner: {result}")
                    else:
                        print("Game is a draw.")
                    break
                game.switch_player()
            else:
                print("No valid moves available. Game over.")
                break


class QLearningAgent:
    def __init__(self):
        self.q_table = defaultdict(lambda: np.zeros(27))  # Using a dictionary to represent the Q-table
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0  # Start with exploration
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.1

    def choose_action(self, state, valid_actions):
        if random.random() < self.epsilon:  # Explore
            return valid_actions.index(random.choice(valid_actions))
        else:  # Exploit
            state_key = self.state_to_key(state)
            return np.argmax(self.q_table[state_key])  # Choose the best action

    def state_to_key(self, state):
        # Flatten the board and convert to a single string
        return ''.join(cell for row in state for cell in row)  # Now it will work

    def update_q_table(self, state, action, reward, next_state, done):
        state_key = self.state_to_key(state)
        next_state_key = self.state_to_key(next_state)

        # Initialize Q-values if the keys do not exist
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(27)  # Assuming 27 possible actions

        best_next_q = 0 if done else np.max(self.q_table[next_state_key])
        # Q-learning update rule
        self.q_table[state_key][action] += self.learning_rate * (
            reward + self.discount_factor * best_next_q - self.q_table[state_key][action]
        )

    def decay_epsilon(self):
        if self.epsilon > self.min_epsilon:
            self.epsilon *= self.epsilon_decay

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)  # Convert defaultdict to dict for serialization

    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)  # Load the dictionary back into q_table


def train_agent(num_episodes):
    playerX = QLearningAgent()
    playerO = QLearningAgent()
    
    # Load the trained Q-table for the agents
    try:
        playerX.load_q_table('q_table_X.pkl')
        print("Loaded Q-table for player X.")
    except FileNotFoundError:
        print("No trained Q-table found for player X.")

    try:
        playerO.load_q_table('q_table_O.pkl')
        print("Loaded Q-table for player O.")
    except FileNotFoundError:
        print("No trained Q-table found for player O.")

    playerTurn = "X"

    start_time = time.time()
    for episode in range(num_episodes):
        game = TicTacToe()  # Reset the game
        state = game.board
        done = False

        while not done:
            # Loop through the board to find valid actions
            valid_actions = game.get_valid_moves()

            if valid_actions:
                # Choose an action based on the current state and valid actions
                if playerTurn == "X":
                    action_index = playerX.choose_action(state, valid_actions)
                elif playerTurn == "O":
                    action_index = playerO.choose_action(state, valid_actions)
                (row, col, size) = valid_actions[action_index]  # Get the row, col, size from valid actions

                # Make a move and get the next state
                game.make_or_replace_move(row, col, size)
                next_state = game.board
                winner = game.check_game_over()

                if winner:
                    if winner == 'X':
                        reward = 1  # X wins
                    else:
                        reward = -1  # O loses
                    done = True
                else:
                    reward = 0  # Continue playing

                playerX.update_q_table(state, action_index, reward, next_state, done)
                playerO.update_q_table(state, action_index, -reward, next_state, done)
                state = next_state  # Update state
            else:
                print("No valid moves available.")
                break  # Exit the loop if there are no valid actions

        playerX.decay_epsilon()  # Decay exploration rate
        playerO.decay_epsilon()  # Decay exploration rate
    
    elapsed_time = time.time() - start_time
    print(format_time(elapsed_time))
    try:
        playerX.save_q_table('q_table_X.pkl')
        playerX.save_q_table('q_table_X_' + str(num_episodes) + '.pkl')
        print("Saved Q-table for player X for ", num_episodes, "games")
    except FileNotFoundError:
        print("Failed to save Q-table for player X for ", num_episodes, "games")

    
    try:
        playerO.save_q_table('q_table_O.pkl')
        playerO.save_q_table('q_table_O_' + str(num_episodes) + '.pkl')
        print("Saved Q-table for player O for ", num_episodes, "games")
    except FileNotFoundError:
        print("Failed to save Q-table for player O for ", num_episodes, "games")
    

def testVSRandom():
    playerX = QLearningAgent()  # Agent X
    playerO = QLearningAgent()  # Agent O
    
    # Load the trained Q-table for the agents
    try:
        playerX.load_q_table('q_table_X.pkl')
        print("Loaded Q-table for player X.")
    except FileNotFoundError:
        print("No trained Q-table found for player X.")

    try:
        playerO.load_q_table('q_table_O.pkl')
        print("Loaded Q-table for player O.")
    except FileNotFoundError:
        print("No trained Q-table found for player O.")

    
    # Prompt the user to choose their character and the agent to play against
    player_choice = input("Choose your random (X or O): ").strip().upper()
    while player_choice not in ['X', 'O']:
        player_choice = input("Invalid choice. Please choose X or O: ").strip().upper()

    random_wins = 0
    ai_wins = 0
    for current_game in range(1000):
        game = TicTacToe()
        # Determine which agent is the opponent
        agent_player = "O" if player_choice == "X" else "X"  # If player is X, agent is O; if player is O, agent is X

        while game.check_game_over() == None:
            # game.print_board()
            # print(f"Current player: {game.current_player} - Remaining counts: {game.remaining_counts()}")

            if game.current_player == player_choice:  # Human player's turn
                valid_actions = game.get_valid_moves()
                action_parts = random.choice(valid_actions)
                if len(action_parts) == 3:
                    row, col, size = action_parts
                    row, col = int(row), int(col)
                    if game.make_or_replace_move(row, col, size):
                        result = game.check_game_over()
                        if result:
                            if result == player_choice:
                                random_wins += 1
                            elif result == agent_player:
                                ai_wins += 1
                            break
                        game.switch_player()
                    else:
                        print("Invalid move or not enough pieces available.")
                else:
                    print("Invalid action.")
            
            else:  # Agent's turn
                valid_actions = game.get_valid_moves()
                if valid_actions:
                    action_index = (playerX if agent_player == "X" else playerO).choose_action(game.board, valid_actions)
                    (row, col, size) = valid_actions[action_index]  # Get the row, col, size from valid actions
                    game.make_or_replace_move(row, col, size)

                    result = game.check_game_over()
                    if result:
                        if result == player_choice:
                            random_wins += 1
                        elif result == agent_player:
                            ai_wins += 1
                        break
                    game.switch_player()
                else:
                    print("No valid moves available. Game over.")
                    break
    print("AI WINS: ", ai_wins, " Random WINS: ", random_wins)

def format_time(seconds):
    minutes = int(seconds // 60)  # Get total minutes
    seconds = int(seconds % 60)    # Get remaining seconds
    return f"{minutes}m {seconds}s"  # Format as "Xm Ys"

def testRandomVSRandom():
    player_choice = "X"

    random_X_wins = 0
    random_O_wins = 0
    for current_game in range(1000):
        game = TicTacToe()
        # Determine which agent is the opponent
        agent_player = "O" if player_choice == "X" else "X"  # If player is X, agent is O; if player is O, agent is X

        while game.check_game_over() == None:
            # game.print_board()
            # print(f"Current player: {game.current_player} - Remaining counts: {game.remaining_counts()}")

            if game.current_player == player_choice:  # RANDOM X player's turn
                valid_actions = game.get_valid_moves()
                action_parts = random.choice(valid_actions)
                if len(action_parts) == 3:
                    row, col, size = action_parts
                    row, col = int(row), int(col)
                    if game.make_or_replace_move(row, col, size):
                        result = game.check_game_over()
                        if result:
                            if result == player_choice:
                                random_X_wins += 1
                            elif result == agent_player:
                                random_O_wins += 1
                            break
                        game.switch_player()
                    else:
                        print("Invalid move or not enough pieces available.")
                else:
                    print("Invalid action.")
            
            else:  # RANDOM O's turn
                valid_actions = game.get_valid_moves()
                action_parts = random.choice(valid_actions)
                if len(action_parts) == 3:
                    row, col, size = action_parts
                    row, col = int(row), int(col)
                    if game.make_or_replace_move(row, col, size):
                        result = game.check_game_over()
                        if result:
                            if result == player_choice:
                                random_X_wins += 1
                            elif result == agent_player:
                                random_O_wins += 1
                            break
                        game.switch_player()
                    else:
                        print("Invalid move or not enough pieces available.")
                else:
                    print("Invalid action.")
            
    print("RAND X WINS: ", random_X_wins, " RAND O WINS: ", random_O_wins)

if __name__ == "__main__":
    
    # Training the agent
    num_games = 100000000

    main()
    # testVSRandom()
    # testRandomVSRandom()
    # train_agent(num_episodes=num_games)

