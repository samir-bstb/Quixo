import copy
#This is our offical Quixo bot, it's designed to play efficiently, optimized and above all, by the rules. 
#Ton Roi uses minimax algorithm improved by alpha-beta pruning, its decision-making is aided by a heuristic function.
#The heuristic funtion is focused on winnig and proritazes the options where it can make lines, nonetheless, it also looks
#for options to block its opponent which makes it a strong adversary to its enemies.

class QuixoBot:
    def __init__(self, symbol):
        self.name = "Ton Roi" #Official Name
        #self.name = "Ahorcarucas" #on honor to its original name
        self.symbol = symbol
        self.opponent_symbol = -symbol
        self.forbidden_moves = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        self.directions = ['l', 'r', 'u', 'd']

    def play_turn(self, board):
        best_move, best_direction = self.get_best_move(board)
        if best_move:
            row, col = best_move
            print("Best move: ", best_move, "Best direction: ", best_direction)
            self.apply_final_move(board, row, col, best_direction)
        return board

    def get_best_move(self, board):
        best_score = -float('inf')
        best_move = ()
        alpha = -float('inf')
        beta = float('inf')
        best_direction = None
        for i in range(5):
            for j in range(5):
                if (i, j) not in self.forbidden_moves:
                    if board[i][j] == 0 or board[i][j] == self.symbol:
                        for direction in self.directions:
                            board_copy = copy.deepcopy(board)
                            if board[i][j] == 0:
                                board_copy[i][j] = self.symbol
                            if self.apply_move(board_copy, i, j, direction):
                                score = self.minimax_alpha_beta(board_copy, 0, alpha, beta, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j)
                                    best_direction = direction
        return best_move, best_direction

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing):
        winner = self.check_winner(board)
        if winner is not None:
            if winner == self.symbol:
                return 10 - depth
            elif winner == 0:
                return 0
            else:
                return depth - 10

        if depth >= 2:
            return self.evaluate_board(board)

        if is_maximizing:
            best_score = -float('inf')
            for i in range(5):
                for j in range(5):
                    if (i, j) not in self.forbidden_moves:
                        if board[i][j] == 0 or board[i][j] == self.symbol:
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board)
                                if board[i][j] == 0:
                                    board_copy[i][j] = self.symbol
                                if self.apply_move(board_copy, i, j, direction):
                                    score = self.minimax_alpha_beta(board_copy, depth + 1, alpha, beta, False)
                                    best_score = max(best_score, score)
                                    alpha = max(alpha, best_score)
                                    if beta <= alpha:
                                        break
            return best_score
        else:
            best_score = float('inf')
            for i in range(5):
                for j in range(5):
                    if (i, j) not in self.forbidden_moves:
                        if board[i][j] == 0 or board[i][j] == self.opponent_symbol:
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board)
                                if board[i][j] == 0:
                                    board_copy[i][j] = self.opponent_symbol
                                if self.apply_move(board_copy, i, j, direction):
                                    score = self.minimax_alpha_beta(board_copy, depth + 1, alpha, beta, True)
                                    best_score = min(best_score, score)
                                    beta = min(beta, best_score)
                                    if beta <= alpha:
                                        break
            return best_score
    #Heuristic Function
    def evaluate_board(self, board):
        # Prioritize winning
        if self.check_winner(board) == self.symbol:
            return 100
        elif self.check_winner(board) == self.opponent_symbol:
            return -100

        score = 0

        # Heuristic: counts opportunities to create lines of 3 or more and blocks opponent
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.symbol:
                    score += self.evaluate_position(board, i, j, self.symbol)
                elif board[i][j] == self.opponent_symbol:
                    score -= self.evaluate_position(board, i, j, self.opponent_symbol)

        return score

    def evaluate_position(self, board, row, col, symbol):
        score = 0

        # Check rows and columns for potential lines
        if row == 0 or row == 4 or col == 0 or col == 4:
            score += 1  # Benefits moves on edges
        if (row, col) in [(0, 0), (0, 4), (4, 0), (4, 4)]:
            score += 2  # Benefits corner moves

        return score

    def apply_move(self, board, row, col, direction): #Applies the moves for minimax
        if direction == "r":
            return self.__move_right(row, col, board)
        elif direction == "l":
            return self.__move_left(row, col, board)
        elif direction == "d":
            return self.__move_down(row, col, board)
        elif direction == "u":
            return self.__move_up(row, col, board)
        return False

    def apply_final_move(self, board, row, col, direction): #Applies the decisive move
        if board[row][col] == 0:
            board[row][col] = self.symbol

        if direction == "r":
            return self.__move_right(row, col, board)
        elif direction == "l":
            return self.__move_left(row, col, board)
        elif direction == "d":
            return self.__move_down(row, col, board)
        elif direction == "u":
            return self.__move_up(row, col, board)
        return False

    # Pieces movement
    def __move_right(self, row, col, board):
        if col < 4:
            Row = board[row]
            aux = Row.pop(col)
            Row.append(aux)
            return True
        else:
            return False

    def __move_left(self, row, col, board):
        if col > 0:
            Row = board[row]
            aux = Row.pop(col)
            Row.insert(0, aux)
            return True
        else:
            return False

    def __move_down(self, row, col, board):
        if row < 4:
            Col = [row[col] for row in board]
            aux = Col.pop(row)
            Col.append(aux)
            for i in range(5):
                board[i][col] = Col[i]
            return True
        else:
            return False

    def __move_up(self, row, col, board):
        if row > 0:
            Col = [row[col] for row in board]
            aux = Col.pop(row)
            Col.insert(0, aux)
            for i in range(5):
                board[i][col] = Col[i]
            return True
        else:
            return False

    #Checks if there's an existing winner
    def check_winner(self, board):
        size = len(board)

        # Check rows and columns
        for i in range(size):
            row_sum = sum(board[i])
            col_sum = sum(board[j][i] for j in range(size))
            if abs(row_sum) == size:
                return board[i][0]
            if abs(col_sum) == size:
                return board[0][i]

        # Check diagonals
        diag_sum1 = sum(board[i][i] for i in range(size))
        diag_sum2 = sum(board[i][size - i - 1] for i in range(size))
        if abs(diag_sum1) == size:
            return board[0][0]
        if abs(diag_sum2) == size:
            return board[0][size - 1]

        if all(board[i][j] != 0 for i in range(size) for j in range(size)):
            return 0  # Indicates a draw

        # No winner
        return None

    #resets bot symbol 
    def reset(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = -symbol
