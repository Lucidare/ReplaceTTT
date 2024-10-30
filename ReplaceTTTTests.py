# test_tic_tac_toe.py
import unittest
from ReplaceTTTSolver import TicTacToe  # Replace with your actual module name

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        self.game = TicTacToe()

    def test_canonical_form(self):
        # Test cases for canonical form
        test_cases = [
            (
                [["sX", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]],

                [[" ", " ", " "],
                [" ", " ", " "],
                ["sX", " ", " "]]
            ),
            (
                [["sX", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]],

                [[" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", "sX"]]
            ),
            (
                [["sO", " ", "sX"],
                [" ", "mX", " "],
                [" ", "lO", " "]],

                [["sO", " ", " "],
                [" ", "mX", "lO"],
                ["sX", " ", " "]]
            ),
            (
                [["sO", " ", "sX"],
                [" ", "mX", " "],
                [" ", "lO", " "]],

                [[" ", "lO", " "],
                [" ", "mX", " "],
                ["sX", " ", "sO"]]
            ),
            (
                [["sO", " ", "sX"],
                [" ", "mX", " "],
                [" ", "lO", " "]],

                [[" ", " ", "sX"],
                ["lO", "mX", " "],
                [" ", " ", "sO"]]
            ),
            # Add more test cases as needed
        ]

        for board_state1, board_state2 in test_cases:
            \
            board_str1 = ''.join(''.join(row) for row in board_state1)
            encoded_board1 = self.game.encoded_board(board_str1)
            canonical_form1 = self.game.canonical_form(encoded_board1)

            board_str2 = ''.join(''.join(row) for row in board_state2)
            encoded_board2 = self.game.encoded_board(board_str2)
            canonical_form2 = self.game.canonical_form(encoded_board2)
            self.assertEqual(canonical_form1, canonical_form2)

    def test_encoded_board_key(self):
        # Test cases for encoded board key
        test_cases = [
            (
                [["sX", " ", " "],
                [" ", "mO", " "],
                [" ", " ", "lX"]],
                "001000000000110000000000011"
            ),
            (
                [["sO", " ", "sX"],
                [" ", "mX", " "],
                [" ", "lO", " "]],
                "101000001000010000000111000"
            ),
            (
                [[" ", " ", " "],
                [" ", " ", " "],
                [" ", " ", " "]],
                "000000000000000000000000000"
            ),
            (
                [[" ", "sX", " "],
                ["mO", " ", "lX"],
                [" ", " ", "sO"]],
                "000001000110000011000000101"
            ),
            (
                [["sX", "sX", "sX"],
                [" ", " ", " "],
                [" ", " ", " "]],
                "001001001000000000000000000"
            ),
            (
                [["mO", " ", " "],
                [" ", "lX", " "],
                [" ", " ", "sO"]],
                "110000000000011000000000101"
            )
        ]

        for index, (board_state, expected) in enumerate(test_cases):
            board_str = ''.join(''.join(row) for row in board_state)
            encoded_key = self.game.encoded_board(board_str)
            self.assertEqual(
                encoded_key,
                expected,
                f"Test case {index + 1} failed: expected {expected}, got {encoded_key} for board state {board_state}"
            )

    def test_encoded_counts(self):
        # Test cases for encoded counts
        test_cases = [
            ("332332", "111110111110"),
            ("332331", "111110111101"),
            ("331332", "111101111110"),
            ("331331", "111101111101"),
            ("330331", "111100111101"),
            ("030030", "001100001100"),
            ("030300", "001100110000"),
            ("002002", "000010000010"),
            ("001001", "000001000001"),
            ("002222", "000010101010"),
            ("100010", "010000000100"),
            ("110000", "010100000000"),
            ("111111", "010101010101"),
            ("300300", "110000110000"),
            ("000000", "000000000000"),
            ("020201", "001000100001"),
            ("222000", "101010000000"),
            ("121212", "011001100110"),
        ]

        for counts, expected in test_cases:
            result = self.game.encoded_counts(counts)
            self.assertEqual(result, expected, f"Failed for counts: {counts}. Expected: {expected}, Got: {result}")

if __name__ == '__main__':
    unittest.main()
