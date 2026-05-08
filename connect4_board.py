import math
import random

class Connect4:
    def __init__(self):
        self.grid = [[0, 0, 0, 0, 0, 0, 0] for _ in range(6)]

    def print_board(self):
        for row in self.grid:
            print(row)
        print("---------------------")

    def drop_piece(self, row, col, player_number):
        self.grid[row][col] = player_number

    def undo_piece(self, row, col):
        self.grid[row][col] = 0

    def is_column_not_full(self, col):
        return self.grid[0][col] == 0

    def get_empty_row(self, col):
        for r in range(5, -1, -1):
            if self.grid[r][col] == 0:
                return r
        return None

    def get_available_columns(self):
        available = []
        for col in range(7):
            if self.is_column_not_full(col):
                available.append(col)
        return available

    def check_winner(self, player_number):
        for c in range(4):
            for r in range(6):
                if self.grid[r][c] == player_number and self.grid[r][c+1] == player_number and self.grid[r][c+2] == player_number and self.grid[r][c+3] == player_number:
                    return True

        for c in range(7):
            for r in range(3):
                if self.grid[r][c] == player_number and self.grid[r+1][c] == player_number and self.grid[r+2][c] == player_number and self.grid[r+3][c] == player_number:
                    return True

        for c in range(4):
            for r in range(3):
                if self.grid[r][c] == player_number and self.grid[r+1][c+1] == player_number and self.grid[r+2][c+2] == player_number and self.grid[r+3][c+3] == player_number:
                    return True

        for c in range(4):
            for r in range(3, 6):
                if self.grid[r][c] == player_number and self.grid[r-1][c+1] == player_number and self.grid[r-2][c+2] == player_number and self.grid[r-3][c+3] == player_number:
                    return True
        return False
      
