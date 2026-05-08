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


class MinimaxAI:
    def minimax(self, board, depth, is_ai_turn):
        if board.check_winner(2): 
            return None, 1000000
        if board.check_winner(1): 
            return None, -1000000
        
        available_cols = board.get_available_columns()
        if len(available_cols) == 0 or depth == 0: 
            return None, 0 

        if is_ai_turn:
            best_score = -math.inf 
            best_col = random.choice(available_cols) 
            
            for col in available_cols:
                row = board.get_empty_row(col)
                board.drop_piece(row, col, 2)
                score = self.minimax(board, depth-1, False)[1]
                board.undo_piece(row, col)
                
                if score > best_score:
                    best_score = score
                    best_col = col
            return best_col, best_score

        else:
            best_score = math.inf 
            best_col = random.choice(available_cols)
            
            for col in available_cols:
                row = board.get_empty_row(col)
                board.drop_piece(row, col, 1) 
                score = self.minimax(board, depth-1, True)[1]
                board.undo_piece(row, col)
                
                if score < best_score:
                    best_score = score
                    best_col = col
            return best_col, best_score


class GameManager:
    def start(self):
        board = Connect4()
        ai = MinimaxAI()
        print("Welcome to Connect 4!")
        board.print_board()

        while True:
            try:
                user_col = int(input("Player 1, make your selection (0-6): "))
                if user_col < 0 or user_col > 6 or not board.is_column_not_full(user_col):
                    print("Invalid input or column full, try again!")
                    continue
            except ValueError:
                print("Please enter a valid number!")
                continue

            row = board.get_empty_row(user_col)
            board.drop_piece(row, user_col, 1)
            board.print_board()

            if board.check_winner(1):
                print("Player 1 Wins!")
                break
            if len(board.get_available_columns()) == 0:
                print("Draw!")
                break

            print("Player 2 is thinking...")
            ai_col, _ = ai.minimax(board, 4, True) 
            ai_row = board.get_empty_row(ai_col)
            board.drop_piece(ai_row, ai_col, 2)
            board.print_board()

            if board.check_winner(2):
                print("Player 2 Wins!")
                break
            if len(board.get_available_columns()) == 0:
                print("Draw!")
                break

if __name__ == "__main__":
    game = GameManager()
    game.start()