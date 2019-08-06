from os import system, name
from random import randrange

class Cell:
    def __init__(self):
        self.value = 0
        self.type = "unoccupied"
        self.is_revealed = False

    def set_mine(self):
        self.value = "*"
        self.type = "mine"

    def set_as_starter(self):
        self.type = "starter"


class Board:
    def __init__(self, num_rows, num_columns, num_mines):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.num_mines = num_mines
        

        self.reset()

    def __repr__(self):
        board_representation = "  "
        for column in range(self.num_columns):
            board_representation += f"{column} "
        board_representation += "\n"
        
        for row in range(self.num_rows):
            board_representation += f"{row}|"
            for column in range(self.num_columns):
                cell = self.board[row][column]
                if cell.is_revealed == False:
                    board_representation += "#|"
                    continue

                if cell.value == 0:
                    board_representation += " |"
                else:
                    board_representation += f"{cell.value}|"
            board_representation += "\n"
        return board_representation

    def reset(self):
        self.board = []
        self.state = "initial"
        self.num_hidden_cells = self.num_rows * self.num_columns
        for _ in range(self.num_rows):
            row_of_cells = []
            for _ in range(self.num_columns):
                row_of_cells.append(Cell())
            self.board.append(row_of_cells)

    def is_game_over(self):
        return self.state == "lose" or self.state == "win"

    def _reveal_all(self):
        for row in range(self.num_rows):
            for column in range(self.num_columns):
                cell = self.board[row][column]
                cell.is_revealed = True

    def reveal_cell(self, row_to_reveal, column_to_reveal):
        cell_to_reveal = self.board[row_to_reveal][column_to_reveal]
        if cell_to_reveal.is_revealed:
            return
        
        if self.state == "initial":
            self._set_starter_area(row_to_reveal, column_to_reveal)
            self._generate_mines()
            self.state = "in progress"
        
        if cell_to_reveal.type == "mine":
            self.state = "lose"
            return
        else:
            cell_to_reveal.is_revealed = True
            self.num_hidden_cells -= 1
            if cell_to_reveal.value == 0:
                self._reveal_contiguous_area(row_to_reveal, column_to_reveal)

        if self.num_hidden_cells == self.num_mines:
            self.state = "win"                
            
    def _reveal_contiguous_area(self, row_to_reveal, column_to_reveal):
        for row_delta in range(-1,2):
            for column_delta in range(-1,2):
                row, column = row_to_reveal-row_delta, column_to_reveal-column_delta
                if row == row_to_reveal and column == column_to_reveal:
                    continue
                if not self._is_coordinate_within_bounds(row, column):
                    continue
                    
                cell = self.board[row][column]
                if cell.is_revealed:
                    continue

                self.num_hidden_cells -= 1
                cell.is_revealed = True
                if cell.value == 0:
                    self._reveal_contiguous_area(row, column)

    def _set_starter_area(self, initial_row, initial_column):
        for row_delta in range(-1,3):
            for column_delta in range(-1,3):
                row, column = initial_row-row_delta, initial_column-column_delta
                if self._is_coordinate_within_bounds(row, column):
                    cell = self.board[row][column]
                    cell.set_as_starter()

    def _is_coordinate_within_bounds(self, row, column):
        return 0 <= row < self.num_rows and 0 <= column < self.num_columns
        
    def _generate_mines(self):
        num_mines_generated = 0
        while num_mines_generated < self.num_mines:
            row_for_mine = randrange(0, self.num_rows)
            column_for_mine = randrange(0, self.num_columns)
            
            cell = self.board[row_for_mine][column_for_mine]
            if cell.type != "unoccupied":
                continue

            cell.set_mine()
            self._update_surrounding_cells_of_mine(row_for_mine, column_for_mine)
            num_mines_generated += 1

    def _update_surrounding_cells_of_mine(self, row_for_mine, column_for_mine):
        for row_delta in range(-1,2):
            for column_delta in range(-1,2):
                row, column = row_for_mine-row_delta, column_for_mine-column_delta
                if not self._is_coordinate_within_bounds(row, column):
                    continue
                cell = self.board[row][column]
                if cell.type == "mine":
                    continue
                cell.value += 1


def clear():
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

if __name__ == "__main__":
    beginner_board = Board(num_rows=9, num_columns=9, num_mines=10)
    while not beginner_board.is_game_over():
        clear()
        print(beginner_board)
        row = int(input("Row: "))
        if row == -1:
            break
        column = int(input("Column: "))
        if column == -1:
            break
        beginner_board.reveal_cell(row, column)
        
    message = ""
    if beginner_board.state == "lose":
        beginner_board._reveal_all()
        print(beginner_board)
        message = "You lose"
    else:
        message = "You win!"

    print(beginner_board)
    print(message)
