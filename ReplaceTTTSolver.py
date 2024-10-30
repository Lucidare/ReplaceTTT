import pickle
import os
import time

class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.counts = {
            "X": {"s": 3, "m": 3, "l": 2},
            "O": {"s": 3, "m": 3, "l": 2}
        }
        self.current_player = "X"  # default with player X
        
        self.memo_file_path = "full_search_updated.pkl"  # Use .pkl for pickle
        self.memo = self.load_memoization()  # Load memoization on initialization


    def load_memoization(self):
        if os.path.exists(self.memo_file_path):
            with open(self.memo_file_path, "rb") as file:
                return pickle.load(file)
        return {}

    def save_memoization(self):
        with open(self.memo_file_path, "wb") as file:
            pickle.dump(self.memo, file)

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

        # Check if the new size is larger than the old size, 
        # if the new size is available, and if the piece belongs to the opponent
        return (size_order[new_size] > size_order[old_size] and
                self.counts[self.current_player][new_size] > 0 and
                old_piece[1] != self.current_player)  # Ensure it's the opponent's piece

    def make_move(self, row, col, size):
        original_piece = self.board[row][col]
        self.board[row][col] = f"{size}{self.current_player}"
        self.counts[self.current_player][size] -= 1
        self.switch_player()
        return original_piece

    def revert_move(self, row, col, size, original_piece):
        self.switch_player()
        self.board[row][col] = original_piece
        self.counts[self.current_player][size] += 1


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
                            if self.counts[self.current_player][size] > 0 and self.can_replace(current_piece, size):
                                valid_moves.append((i, j, size))  # Add (row, col, size) as a valid replacement move

        return valid_moves

    def check_game_over(self):
        winner = self.check_connect_3()

        if winner:
            return winner
        if self.is_full() or not self.get_valid_moves():
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

    def board_key(self):
        # Convert the board into a string representation
        board_str = ''.join(''.join(row) for row in self.board)
        
        # Convert the counts into a string representation
        counts_str = ''.join(f"{count}" for player, sizes in self.counts.items() for count in sizes.values())
        return f"{board_str}|{counts_str}"

    def encoded_game_state(self):
        # Obtain the board_key string
        board_str_key = self.board_key()

        # Convert the board portion
        board_part, counts_part = board_str_key.split("|")

        board_binary = self.encoded_board(board_part)
        normalized_board_binary = self.canonical_form(board_binary)
        counts_binary = self.encoded_counts(counts_part)

        # Combine board and counts into one binary string
        full_binary_key = normalized_board_binary + counts_binary
        # return full_binary_key
        return int(full_binary_key, 2)

    def encoded_board(self, board):
        # Map pieces from the board key string to binary
        piece_map = {
            " ": "000",        # Empty cell: 000
            "sX": "001",       # Small X
            "mX": "010",       # Medium X
            "lX": "011",       # Large X
            "sO": "101",       # Small O
            "mO": "110",       # Medium O
            "lO": "111"        # Large O
        }
        
        board_binary = board
        for piece, binary in piece_map.items():
            board_binary = board_binary.replace(piece, binary)
        return board_binary

    def encoded_counts(self, counts):
        # Create a mapping from digit to its binary representation (2 bits)
        binary_mapping = {
            '0': '00',
            '1': '01',
            '2': '10',
            '3': '11'
        }

        # Initialize a variable for the binary representation
        counts_binary = counts

        # Replace each digit in the counts string using the binary mapping
        for digit in sorted(binary_mapping.keys()):  # Sort keys for ascending order
            counts_binary = counts_binary.replace(digit, binary_mapping[digit])  # Replace in order
        return counts_binary


    
    # Find same boards that are just flipped/mirrored to minimize redundant search
    def canonical_form(self, board_binary):
        # Define transformations with index mappings
        transformations = [
            [0, 1, 2,   # Original
            3, 4, 5,
            6, 7, 8],
            
            [6, 3, 0,   # 90° Rotation
            7, 4, 1,
            8, 5, 2],
            
            [8, 7, 6,   # 180° Rotation
            5, 4, 3,
            2, 1, 0],
            
            [2, 5, 8,   # 270° Rotation
            1, 4, 7,
            0, 3, 6],
            
            [2, 1, 0,   # Horizontal Flip
            5, 4, 3,
            8, 7, 6],
            
            [6, 7, 8,   # Vertical Flip
            3, 4, 5,
            0, 1, 2],
            
            [0, 3, 6,   # Diagonal (\) Flip
            1, 4, 7,
            2, 5, 8],
            
            [8, 5, 2,   # Diagonal (/) Flip
            7, 4, 1,
            6, 3, 0]
        ]

        # Convert `board_binary` into chunks of 3 bits per cell
        board_cells = [board_binary[i:i+3] for i in range(0, len(board_binary), 3)]
        
        # Apply each transformation and store the resulting strings
        transformed_boards = []

        for transformation in transformations:
            transformed_board = ''.join(board_cells[i] for i in transformation)
            transformed_boards.append(transformed_board)

        # Find the lexicographically smallest transformation
        smallest_board = min(transformed_boards)
        
        # Return the smallest board configuration as a binary string
        return smallest_board


    def minimax(self, depth, is_maximizing):
        board_state = self.encoded_game_state()
        if board_state in self.memo:
            return self.memo[board_state]

        winner = self.check_game_over()
        if winner == "X":
            # self.save_memoization()
            return 10 - depth  # Favor wins that occur sooner
        elif winner == "O":
            # self.save_memoization()
            return depth - 10  # Favor losses that occur later
        elif winner == "IMPOSSIBLE":  # Draw case
            # self.save_memoization()
            return 0

        if is_maximizing:
            max_eval = float('-inf')
            for (row, col, size) in self.get_valid_moves():
                original_piece = self.make_move(row, col, size)
                eval = self.minimax(depth + 1, False)
                self.revert_move(row, col, size, original_piece)
                max_eval = max(max_eval, eval)
            self.memo[board_state] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for (row, col, size) in self.get_valid_moves():
                original_piece = self.make_move(row, col, size)
                eval = self.minimax(depth + 1, True)
                self.revert_move(row, col, size, original_piece)
                min_eval = min(min_eval, eval)
            self.memo[board_state] = min_eval
            return min_eval


    def best_move(self, isTimed = False):
        # Initialize best value for max/min depending on player symbol
        best_val = float('-inf') if self.current_player == "X" else float('inf')
        move = None
        is_maximizing = self.current_player == "X"
        for (row, col, size) in self.get_valid_moves():
            if isTimed:
                print("Starting", row, col, size, "move at")
                get_current_date_time()
                start_time = time.time()
            
            original_piece = self.make_move(row, col, size)
            move_val = self.minimax(0, not is_maximizing)
            self.revert_move(row, col, size, original_piece)

            if isTimed:
                elapsed_time = time.time() - start_time
                print("Duration:", format_time(elapsed_time))

                print("Finished", row, col, size, "move at")
                get_current_date_time()

            # Update the best move based on maximizing/minimizing logic
            if (is_maximizing and move_val > best_val) or (not is_maximizing and move_val < best_val):
                best_val = move_val
                move = (row, col, size)
        return move

    def reset(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.counts = {
            "X": {"s": 3, "m": 3, "l": 2},
            "O": {"s": 3, "m": 3, "l": 2}
        }
        self.current_player = "X"  # default with player X
        
    def populate_memoization_table(self, isTimed = False):
        
        if isTimed:
            print("Starting populating at")
            get_current_date_time()
            start_time = time.time()
        # Start the memoization process by calling minimax on the empty board
        self.best_move(isTimed)

        if isTimed:
            elapsed_time = time.time() - start_time
            print("Duration:", format_time(elapsed_time))
            print("Finished populating at")
            get_current_date_time()
        # Duration: 230m 21s when using shelve and print statements for depth < 7
        # Duration: 27m 1s when using int index with pickle no prints

def get_current_date_time():
    # Get the current time in seconds since the Unix epoch
    current_time = time.time()

    # Convert it to a struct_time in the local timezone
    local_time = time.localtime(current_time)

    # Format the struct_time to a readable string
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

    print("Current date and time:", formatted_time)

def format_time(seconds):
    minutes = int(seconds // 60)  # Get total minutes
    seconds = int(seconds % 60)    # Get remaining seconds
    return f"{minutes}m {seconds}s"  # Format as "Xm Ys"


def main():
    game = TicTacToe()

    try:
        # game.populate_memoization_table()  # Populate the table before playing

        human_player = input("Choose your symbol (X or O): ").upper()
        game.current_player = "X"

        game.print_board()
        while game.check_game_over() is None:
            if game.current_player == human_player:
            #     action = input("Enter 'row col size' to place a piece (sizes: s, m, l): ")
            #     row, col, size = map(str, action.split())
            #     row, col = int(row), int(col)
            #     if (row, col, size) not in game.get_valid_moves():
            #         print("Invalid move")
            #         continue
            #     game.make_move(row, col, size)
            #     game.print_board()

                # print(game.get_valid_moves())

                print("AI is making a move...")
                row, col, size = game.best_move()
                game.make_move(row, col, size)
                game.print_board()
            else:
                # action = input("Enter 'row col size' to place a piece (sizes: s, m, l): ")
                # row, col, size = map(str, action.split())
                # row, col = int(row), int(col)
                # if (row, col, size) not in game.get_valid_moves():
                #     print("Invalid move")
                #     continue
                # if game.make_move(row, col, size):
                #     if game.check_game_over():
                #         break

                # print(game.get_valid_moves())

                print("AI is making a move...")
                row, col, size = game.best_move()
                game.make_move(row, col, size)
                game.print_board()
        
        # Print the final board and the game result
        game.print_board()
        winner = game.check_game_over()
        if winner == "X":
            print("You win!")
        elif winner == "O":
            print("AI wins!")
        else:
            print("It's a draw!")
    
    except KeyboardInterrupt:
        print("\nGame interrupted. Saving memoization file...")
    finally:
        game.save_memoization()

if __name__ == "__main__":
    main()