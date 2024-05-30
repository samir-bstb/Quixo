import copy

class QuixoBot:
   
    def __init__(self, symbol):
        self.symbol = symbol
        self.name = ""
        self.forbidden_moves = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
        self.directions = ['l', 'r', 'u', 'd']

    #  0 - blank cubit
    #  1 - X cubit
    # -1 - O cubit

    def play_turn(self, board):
        best_move, best_direction = self.get_best_move(board)
        if best_move:
            row, col = best_move
            print("best move: ",best_move, "best direction: ", best_direction)
            self.apply_move(board, row, col, best_direction)
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
                    if board[i][j] == 0: 
                        #print("enter best move with 0")
                        for direction in self.directions:
                            board_copy = copy.deepcopy(board) 
                            board_copy[i][j] = self.symbol
                            if self.apply_move(board_copy, i, j, direction):
                                score = self.minimax_alpha_beta(board, 0, alpha, beta, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j)
                                    best_direction = direction
                    elif board[i][j] == self.symbol:
                        #print("enter best move with symbol")
                        for direction in self.directions:
                            board_copy = copy.deepcopy(board) 
                            if self.apply_move(board_copy, i, j, direction):
                                score = self.minimax_alpha_beta(board, 0, alpha, beta, False)
                                if score > best_score:
                                    best_score = score
                                    best_move = (i, j)
                                    best_direction = direction
        return best_move, best_direction

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing): #add the smae logic fro the get_best_move function and  miximum depth of 2
        winner = self.check_winner(board)
        if winner is not None:
            if winner == self.symbol:
                return 10 - depth
            elif winner == 0:
                return 0
            else:
                return depth - 10
            
        if depth >= 2:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(5):
                for j in range(5):
                    if (i, j) not in self.forbidden_moves:
                        if board[i][j] == 0: 
                            #print("enter maximizing with 0")
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board) 
                                board_copy[i][j] = self.symbol
                                if self.apply_move(board_copy, i, j, direction):
                                    #print("move" , i, j, direction)
                                    #self.print_board(board_copy)
                                    #print()
                                    score = self.minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                                    best_score = max(best_score, score) 
                                    alpha = max(alpha, best_score)
                                    if beta <= alpha:   
                                        break     
                        elif board[i][j] == self.symbol:
                            #print("enter maximizing with symbol")
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board) 
                                if self.apply_move(board_copy, i, j, direction):
                                    #print("move" , i, j, direction)
                                    #self.print_board(board_copy)
                                    #print()
                                    score = self.minimax_alpha_beta(board, depth + 1, alpha, beta, False)
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
                        if board[i][j] == 0: 
                            #print("enter minimizing with 0")
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board) 
                                board_copy[i][j] = self.symbol
                                if self.apply_move(board_copy, i, j, direction):
                                    #print("move" , i, j, direction)
                                    #self.print_board(board_copy)
                                    #print()
                                    score = self.minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                                    best_score = min(best_score, score) 
                                    beta = min(alpha, best_score)
                                    if beta <= alpha:   
                                        break
            
                        elif board[i][j] == self.symbol:
                            #print("enter minimizing with symbol")
                            for direction in self.directions:
                                board_copy = copy.deepcopy(board) 
                                if self.apply_move(board_copy, i, j, direction):
                                    #print("move" , i, j, direction)
                                    #self.print_board(board_copy)
                                    #print()  
                                    score = self.minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                                    best_score = min(best_score, score) 
                                    beta = min(alpha, best_score)
                                    if beta <= alpha:   
                                        break
            return best_score
        
    def get_possible_moves(self, board):
        moves = []
        for i in range(5):
            for j in range(5):
                if (board[i][j] == 0 or board[i][j] == self.symbol) and (i, j) not in self.forbidden_moves:
                    moves.append((i, j))
        return moves    

    def apply_move(self, board, row, col, direction):
        if direction == "r":
            return self.__move_right(row, col, board)
        elif direction == "l":
            return self.__move_left(row, col, board)
        elif direction == "d":
            return self.__move_down(row, col, board)
        elif direction == "u":
            return self.__move_up(row, col, board)
        return False 

    def print_board(self, board):
        for row in board:
            print(row)

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
        
    def check_winner(self, board): #change it to game over
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
            return 0  # Indicating a draw

        # No winner
        return None
    
    def reset(self, symbol):
        pass

#board = [[0 for _ in range(5)] for _ in range(5)]
board = [[-1, 1, 0, 0,1], 
         [ 1, -1, 1, 1, -1], 
         [-1, 0, -1, 0,1], 
         [ 0, 0, 0, 0, 1], 
         [ 0,-1, 1, 0, 1]]

bot = QuixoBot(1)
print(board)
new_board = bot.play_turn(board)
print(new_board)
