import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

class Connect4Board:
    def __init__(self):
        self.board = [[EMPTY for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[0][col] == EMPTY

    def get_valid_locations(self):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def get_next_open_row(self, col):
        for r in range(ROW_COUNT-1, -1, -1):
            if self.board[r][col] == EMPTY:
                return r
        return None

    def print_board(self):
        print("-" * 21)
        for r in range(ROW_COUNT):
            print(self.board[r])
        print("-" * 21)

    def winning_move(self, piece):
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
        for c in range(COLUMN_COUNT-3):
            for r in range(ROW_COUNT-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
        for c in range(COLUMN_COUNT-3):
            for r in range(3, ROW_COUNT):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
        return False

    def is_terminal_node(self):
        return self.winning_move(PLAYER_PIECE) or self.winning_move(AI_PIECE) or len(self.get_valid_locations()) == 0


class AIAgent:
    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2
        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4
        return score

    def score_position(self, board_obj, piece):
        score = 0
        board = board_obj.board
        center_array = [board[r][COLUMN_COUNT//2] for r in range(ROW_COUNT)]
        center_count = center_array.count(piece)
        score += center_count * 3
        for r in range(ROW_COUNT):
            row_array = board[r]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
        for c in range(COLUMN_COUNT):
            col_array = [board[r][c] for r in range(ROW_COUNT)]
            for r in range(ROW_COUNT-3):
                window = col_array[r:r+WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)
        return score

    def minimax(self, board_obj, depth, alpha, beta, maximizingPlayer):
        valid_locations = board_obj.get_valid_locations()
        is_terminal = board_obj.is_terminal_node()
        if depth == 0 or is_terminal:
            if is_terminal:
                if board_obj.winning_move(AI_PIECE): return (None, 10000000000000)
                elif board_obj.winning_move(PLAYER_PIECE): return (None, -10000000000000)
                else: return (None, 0)
            else:
                return (None, self.score_position(board_obj, AI_PIECE))

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board_obj.get_next_open_row(col)
                b_copy = Connect4Board()
                b_copy.board = [r[:] for r in board_obj.board]
                b_copy.drop_piece(row, col, AI_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return column, value
        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board_obj.get_next_open_row(col)
                b_copy = Connect4Board()
                b_copy.board = [r[:] for r in board_obj.board]
                b_copy.drop_piece(row, col, PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta: break
            return column, value

class GameManager:
    def __init__(self):
        self.board = Connect4Board()
        self.ai = AIAgent()
        self.game_over = False
        self.turn = random.randint(0, 1)

    def play(self):
        print("Welcome to Connect 4 - AI Minimax Edition!")
        self.board.print_board()
        while not self.game_over:
            if self.turn == 0:
                col = -1
                while True:
                    try:
                        col = int(input(f"Player 1, make your selection (0-{COLUMN_COUNT-1}): "))
                        if 0 <= col < COLUMN_COUNT and self.board.is_valid_location(col):
                            break
                        else: print("Invalid input. Try again.")
                    except ValueError:
                        print("Please enter a valid integer.")
                row = self.board.get_next_open_row(col)
                self.board.drop_piece(row, col, PLAYER_PIECE)
                if self.board.winning_move(PLAYER_PIECE):
                    self.board.print_board()
                    print(" PLAYER1 WINS! ")
                    self.game_over = True
                self.turn ^= 1
                if not self.game_over: self.board.print_board()
            elif self.turn == 1 and not self.game_over:
                print(" PLAYER2 is thinking...")
                col, _ = self.ai.minimax(self.board, 5, -math.inf, math.inf, True)
                if self.board.is_valid_location(col):
                    row = self.board.get_next_open_row(col)
                    self.board.drop_piece(row, col, AI_PIECE)
                    if self.board.winning_move(AI_PIECE):
                        self.board.print_board()
                        print(" PLAYER2 WINS! ")
                        self.game_over = True
                    self.turn ^= 1
                    if not self.game_over: self.board.print_board()

if __name__ == "__main__":
    game = GameManager()
    game.play()