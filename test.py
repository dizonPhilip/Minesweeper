import unittest
from minesweeper import Board, Cell

class MinesweeperTest(unittest.TestCase):
    def test_board_init(self):
        board = Board(num_rows=8, num_columns=9, num_mines=10)
        self.assertEqual(8, board.num_rows)
        self.assertEqual(9, board.num_columns)
        self.assertEqual(10, board.num_mines)

    def test_board_reset(self):
        board = Board(num_rows=8, num_columns=9, num_mines=10)
        for row in range(board.num_rows):
            for column in range(board.num_columns):
                cell = board.board[row][column]
                cell.value = 1

        board.reset()
        for row in range(board.num_rows):
            for column in range(board.num_columns):
                cell = board.board[row][column]
                self.assertEqual(0, cell.value)

    def test_board_generate_mines(self):
        board = Board(num_rows=9, num_columns=9, num_mines=10)
        board._generate_mines()
        num_mines_found = 0
        for row in range(board.num_rows):
            for column in range(board.num_columns):
                cell = board.board[row][column]
                if cell.type == "mine":
                    num_mines_found += 1
        self.assertEqual(10, num_mines_found)

    def test_board_starter_area(self):
        board = Board(num_rows=9, num_columns=9, num_mines=10)
        board._set_starter_area(initial_row=1, initial_column=1)
        for row in range(board.num_rows):
            for column in range(board.num_columns):
                cell = board.board[row][column]
                if row in range(0,4) and column in range(0,4):
                    cell.type = "starter"
                else:
                    cell.type = "unoccupied"

if __name__ == "__main__":
    unittest.main()