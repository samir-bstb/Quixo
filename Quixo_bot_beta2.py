class QuixoBot:

    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = -symbol
        self.forbidden_moves = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

    #  0 - blank cubit
    #  1 - X cubit
    # -1 - O cubit

    def play_turn(self, board):
        best_move, best_direction = self.get_best_move(board)
        if best_move:
            row, col = best_move
            print("move ",best_move)
            print("direction ", best_direction)
            self.apply_move(board, row, col, best_direction)
        return board

    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = None
        best_direction = None
        alpha = -float('inf')
        beta = float('inf')

        for i in range(5):
            for j in range(5):
                if (i, j) not in self.forbidden_moves:
                    if board[i][j] == 0:
                        # Try placing a new piece
                        directions = ["left", "right", "up", "down"]
                        for direction in directions:
                            new_board = [row[:] for row in board]  # Make a copy of the board
                            if self.apply_move(new_board, i, j, direction):
                                score = self.minimax(new_board, 0, alpha, beta, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j)
                                    best_direction = direction
        return best_move, best_direction

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if self.check_winner(board, self.symbol):
            return 1
        elif self.check_winner(board, self.opponent_symbol):
            return -1
        elif self.check_draw(board):
            return 0

        if depth >= 2:  # Limit depth for minimax
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        directions = ["left", "right", "up", "down"]
                        for direction in directions:
                            new_board = [row[:] for row in board]
                            if self.apply_move(new_board, i, j, direction):
                                score = self.minimax(new_board, depth + 1, alpha, beta, False)
                                best_score = max(score, best_score)
                                alpha = max(alpha, best_score)
                                if beta <= alpha:
                                    break
            return best_score
        else:
            best_score = float('inf')
            for i in range(5):
                for j in range(5):
                    if board[i][j] == 0:
                        directions = ["left", "right", "up", "down"]
                        for direction in directions:
                            new_board = [row[:] for row in board]
                            if self.apply_move(new_board, i, j, direction):
                                score = self.minimax(new_board, depth + 1, alpha, beta, True)
                                best_score = min(score, best_score)
                                beta = min(beta, best_score)
                                if beta <= alpha:
                                    break
            return best_score

    def apply_move(self, board, row, col, direction):
        if direction == "right":
            return self.__move_right(row, col, board)
        elif direction == "left":
            return self.__move_left(row, col, board)
        elif direction == "down":
            return self.__move_down(row, col, board)
        elif direction == "up":
            return self.__move_up(row, col, board)
        return False

    def __move_right(self, row, col, board):
        if col < 4:
            board[row][col] = self.symbol
            Row = board[row]
            aux = Row.pop(col)
            Row.append(aux)
            return True
        return False

    def __move_left(self, row, col, board):
        if col > 0:
            board[row][col] = self.symbol
            Row = board[row]
            aux = Row.pop(col)
            Row.insert(0, aux)
            return True
        return False

    def __move_down(self, row, col, board):
        if row < 4:
            board[row][col] = self.symbol
            Col = [row[col] for row in board]
            aux = Col.pop(row)
            Col.append(aux)
            for i in range(5):
                board[i][col] = Col[i]
            return True
        return False

    def __move_up(self, row, col, board):
        if row > 0:
            board[row][col] = self.symbol
            Col = [row[col] for row in board]
            aux = Col.pop(row)
            Col.insert(0, aux)
            for i in range(5):
                board[i][col] = Col[i]
            return True
        return False

    def check_winner(self, board, player):
        for i in range(5):
            if all([board[i][j] == player for j in range(5)]):
                return True
            if all([board[j][i] == player for j in range(5)]):
                return True
        if all([board[i][i] == player for i in range(5)]) or all([board[i][4 - i] == player for i in range(5)]):
            return True
        return False

    def check_draw(self, board):
        return all([all([cell != 0 for cell in row]) for row in board])

    def reset(self, symbol):
        pass

    def print_board(self, board):
        for row in board:
            print(row)

# Example usage
board = [[-1, 1, 0, 0,-1], 
         [ 0, 1, 1, 1, 0], 
         [-1, 0, 0, 0,-1], 
         [ 0, 0, 0, 0, 0], 
         [ 0,-1, 1, 0, 0]]
bot = QuixoBot(1)
new_board = bot.play_turn(board)
bot.print_board(new_board)
