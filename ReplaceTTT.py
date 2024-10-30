class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.counts = {
            "X": {"s": 3, "m": 3, "l": 2},
            "O": {"s": 3, "m": 3, "l": 2}
        }
        self.current_player = "X"

    def print_board(self):
        for row in self.board:
            print(" | ".join(row))
            print("-" * 9)

    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]
        return None

    def is_full(self):
        return all(cell != " " for row in self.board for cell in row)

    def make_or_replace_move(self, row, col, size):
        current_piece = self.board[row][col]
        
        # If the cell is empty, make a move
        if current_piece == " ":
            if self.counts[self.current_player][size] > 0:
                self.board[row][col] = f"{size}{self.current_player}"  # E.g., 'sX', 'mX', 'lX'
                self.counts[self.current_player][size] -= 1
                return True
        
        # If the cell is occupied, check for replacement
        elif current_piece[1] != self.current_player and self.can_replace(current_piece, size):
            self.counts[self.current_player][size] -= 1
            self.counts[self.current_player][current_piece[0]] += 1
            self.board[row][col] = f"{size}{self.current_player}"
            return True
        
        return False

    def can_replace(self, old_piece, new_size):
        return (new_size != old_piece[0] and
                self.counts[self.current_player][new_size] > 0)

    def remaining_counts(self):
        return self.counts

    def get_winner_or_counts(self):
        winner = self.check_winner()
        if winner:
            return winner
        if self.is_full():
            return self.remaining_counts()
        return None

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

# Example usage
if __name__ == "__main__":
    game = TicTacToe()
    
    while True:
        game.print_board()
        print(f"Current player: {game.current_player} - Remaining counts: {game.remaining_counts()}")
        
        action = input("Enter 'row col size' to place or replace (sizes: s, m, l): ")
        action_parts = action.split()
        
        if len(action_parts) == 3:
            row, col, size = action_parts
            row, col = int(row), int(col)
            if not game.make_or_replace_move(row, col, size):
                print("Invalid move or replacement.")
        else:
            print("Invalid action.")

        result = game.get_winner_or_counts()
        if result:
            game.print_board()
            if isinstance(result, str):
                print(f"Winner: {result}")
            else:
                print("Game is a draw. Remaining counts:", result)
            break
        
        game.switch_player()
