import math
import random

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
    # الكلاس الثالث: تشغيل اللعبة وتنظيم الأدوار
    def start(self):
        board = Connect4()
        ai = MinimaxAI()
        print("Welcome to Connect 4!")
        board.print_board()

        while True:
            # دور الإنسان (Player 1)
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

            # دور الكمبيوتر (Player 2)
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