import tkinter as tk
from tkinter import messagebox
from ReplaceTTTSolver import TicTacToe  # Ensure this is the correct import

class ReplaceTTTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.setup_game()

    def setup_game(self):
        self.game = TicTacToe()
        self.game_over = False
        self.selected_size = "s"
        self.piece_map = {
            "sX": "Small X", "mX": "Medium X", "lX": "Large X",
            "sO": "Small O", "mO": "Medium O", "lO": "Large O",
            " ": " "
        }
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        self.setup_gui()
        self.choose_symbol()

    def setup_gui(self):
        # Create the board for Tic Tac Toe
        board_frame = tk.Frame(self.root)
        board_frame.grid(row=0, column=0, padx=10, pady=10)

        for row in range(3):
            for col in range(3):
                button = tk.Button(board_frame, text=" ", width=10, height=3,
                                   command=lambda r=row, c=col: self.handle_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        # Create a frame for size selection with counts
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=1, padx=10, pady=10)

        # Add size selection buttons with counts
        self.size_buttons = {}
        for size in ["s", "m", "l"]:
            btn = tk.Button(control_frame, text=f"{size.upper()} ({self.game.counts[self.game.current_player][size]})", 
                            width=10, height=2,
                            command=lambda s=size: self.select_size(s))
            btn.pack(pady=5)
            self.size_buttons[size] = btn

        # Label to display the current selection
        self.selection_label = tk.Label(control_frame, text=f"Current Selection: {self.selected_size.upper()}", font=("Arial", 10))
        self.selection_label.pack(pady=10)

        # Add a restart/quit button
        self.restart_button = tk.Button(control_frame, text="Restart", command=self.restart, width=10, height=2)
        self.restart_button.pack(pady=5)

        # Initially set the selected size button's color and relief
        self.update_size_buttons()

    def choose_symbol(self):
        # Prompt the player to choose a symbol
        isPlayFirst = messagebox.askyesno("Choose Symbol", "Do you want to go first as X?")
        if not isPlayFirst:
            self.ai_move()
            self.update_board()

    def select_size(self, size):
        if self.game_over:
            return
        self.selected_size = size
        self.update_size_buttons()

    def handle_click(self, row, col):
        if self.game_over:
            return
        size = self.selected_size

        if (row, col, size) not in self.game.get_valid_moves():
            self.selection_label.config(text="Invalid Move: You cannot place that piece here.")
            return
        
        self.game.make_move(row, col, size)
        self.update_board()
        
        if winner := self.game.check_game_over():
            self.display_winner(winner)
            return
        
        self.ai_move()
        self.update_board()
        if winner := self.game.check_game_over():
            self.display_winner(winner)
            return

        self.update_size_buttons()

    def ai_move(self):
        # Make the best move for the AI
        row, col, size = self.game.best_move()
        self.game.make_move(row, col, size)
        self.update_board()

    def update_board(self):
        # Update the text of each button to reflect the current board state
        for row in range(3):
            for col in range(3):
                piece = self.game.board[row][col]
                self.buttons[row][col].config(text=self.piece_map[piece])

    def update_size_buttons(self):
        # Highlight the selected size button and "press" it down
        for size, btn in self.size_buttons.items():
            relief = tk.SUNKEN if size == self.selected_size else tk.RAISED
            btn.config(relief=relief, text=f"{size.upper()} ({self.game.counts[self.game.current_player][size]})")
        
        # Update the label with the current selection
        self.selection_label.config(text=f"Current Selection: {self.selected_size.upper()}")

    def display_winner(self, winner):
        self.game_over = True
        if winner == "X":
            msg = "X wins!"
        elif winner == "O":
            msg = "O wins!"
        else:
            msg = "It's a draw!"
        
        # Display winner message and set the label to show the winner
        self.selection_label.config(text=msg)  # Update label to show winner
        self.update_board()

    def reset_game(self):
        self.game_over = False
        # Reset the game state and GUI for a new game
        self.game.reset()  # Make sure your TicTacToe class has a reset method
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")
        self.selected_size = "s"
        self.selection_label.config(text=f"Current Selection: {self.selected_size.upper()}")  # Reset the label to show current selection
        for size in self.size_buttons:
            self.size_buttons[size].config(relief=tk.RAISED)

        self.update_size_buttons()
        self.choose_symbol()

    def restart(self):
        # This function handles quitting the application or restarting the game
        self.reset_game()  # Restart the game, or you can use self.root.quit() to quit the app

if __name__ == "__main__":
    root = tk.Tk()
    app = ReplaceTTTGUI(root)
    root.mainloop()
